/* Globe de la fiche : carte du monde des titres suivis (D-20261123-4, choix du propriétaire du 22/11/2026).
   Inséré dans la page par rendu.py, dans un bloc <script> à part dont l'empreinte (CSP) est calculée comme
   celle du script principal. Lit D.globe (scripts/globe.py) et, seulement quand on arrive à la section, le
   tracé des pays (Natural Earth, domaine public) dans globe/ : aucun service extérieur, rien n'est envoyé.
   Sans page (tests.py, avec node ou JavaScriptCore), il expose seulement ses calculs dans GlobeMath. */
(function () {
  "use strict";
  const RAD = Math.PI / 180;

  // ---------- calculs (testés sans page) ----------

  // Tracé compact (trace_pays.py) → pays avec, pour chaque polygone, ses anneaux en degrés (ll) et en points
  // de la sphère (xyz), une calotte qui l'englobe (pour ne pas dessiner ce qui est hors de vue) et sa boîte.
  function decoder(liste) {
    return (liste || []).map((x) => {
      const polys = [];
      for (const anneaux of x.p || []) {
        const rings = [];
        for (const a of anneaux) {
          const n = a.length >> 1;
          if (n < 3) continue;
          const ll = new Float64Array(2 * n), xyz = new Float64Array(3 * n);
          let lo = 0, la = 0;
          for (let i = 0; i < n; i++) {
            lo += a[2 * i]; la += a[2 * i + 1];
            const L = lo / 100, P = la / 100, cp = Math.cos(P * RAD);
            ll[2 * i] = L; ll[2 * i + 1] = P;
            xyz[3 * i] = cp * Math.cos(L * RAD); xyz[3 * i + 1] = cp * Math.sin(L * RAD); xyz[3 * i + 2] = Math.sin(P * RAD);
          }
          rings.push({ n, ll, xyz });
        }
        if (!rings.length) continue;
        const e = rings[0];
        let sx = 0, sy = 0, sz = 0, b0 = 180, b1 = 90, b2 = -180, b3 = -90;
        for (let i = 0; i < e.n; i++) {
          sx += e.xyz[3 * i]; sy += e.xyz[3 * i + 1]; sz += e.xyz[3 * i + 2];
          const L = e.ll[2 * i], P = e.ll[2 * i + 1];
          if (L < b0) b0 = L; if (L > b2) b2 = L; if (P < b1) b1 = P; if (P > b3) b3 = P;
        }
        const nn = Math.hypot(sx, sy, sz) || 1;
        sx /= nn; sy /= nn; sz /= nn;
        let rayon = 0;
        for (let i = 0; i < e.n; i++) {
          const d = sx * e.xyz[3 * i] + sy * e.xyz[3 * i + 1] + sz * e.xyz[3 * i + 2];
          rayon = Math.max(rayon, Math.acos(Math.max(-1, Math.min(1, d))));
        }
        polys.push({ rings, c: [sx, sy, sz], rayon, box: [b0, b1, b2, b3] });
      }
      return { c: x.c || "", n: x.n || "", l: x.l || [0, 0], r: x.r || 0, polys };
    }).filter((f) => f.polys.length);
  }

  // Rotation qui amène le point (lon0, lat0) au centre du disque, nord en haut. Lignes : x, y (écran) et z
  // (vers l'observateur : un point est sur la face visible si z > 0).
  function matrice(lon0, lat0) {
    const l = lon0 * RAD, p = lat0 * RAD, sl = Math.sin(l), cl = Math.cos(l), sp = Math.sin(p), cp = Math.cos(p);
    return [-sl, cl, 0, -sp * cl, -sp * sl, cp, cp * cl, cp * sl, sp];
  }
  function projeter(M, lon, lat) {  // → [x, y, z] sur la sphère unité tournée
    const L = lon * RAD, P = lat * RAD, cp = Math.cos(P), X = cp * Math.cos(L), Y = cp * Math.sin(L), Z = Math.sin(P);
    return [M[0] * X + M[1] * Y + M[2] * Z, M[3] * X + M[4] * Y + M[5] * Z, M[6] * X + M[7] * Y + M[8] * Z];
  }
  // Point du disque (u, v en rayons du globe, v vers le haut) → [lon, lat], ou null hors du globe
  function inverse(M, u, v) {
    const r2 = u * u + v * v;
    if (r2 > 1) return null;
    const w = Math.sqrt(1 - r2);
    const X = M[0] * u + M[3] * v + M[6] * w, Y = M[1] * u + M[4] * v + M[7] * w, Z = M[2] * u + M[5] * v + M[8] * w;
    return [Math.atan2(Y, X) / RAD, Math.asin(Math.max(-1, Math.min(1, Z))) / RAD];
  }
  function dansAnneau(lon, lat, ll, n) {  // test du rayon, en lon/lat (Natural Earth coupe les pays à ±180°)
    let c = false;
    for (let i = 0, j = n - 1; i < n; j = i++) {
      const yi = ll[2 * i + 1], yj = ll[2 * j + 1];
      if ((yi > lat) !== (yj > lat)) {
        const xi = ll[2 * i], xj = ll[2 * j];
        if (lon < (xj - xi) * (lat - yi) / (yj - yi) + xi) c = !c;
      }
    }
    return c;
  }
  function dansPoly(lon, lat, p) {
    const b = p.box;
    if (lon < b[0] || lon > b[2] || lat < b[1] || lat > b[3]) return false;
    if (!dansAnneau(lon, lat, p.rings[0].ll, p.rings[0].n)) return false;
    for (let k = 1; k < p.rings.length; k++) if (dansAnneau(lon, lat, p.rings[k].ll, p.rings[k].n)) return false;
    return true;
  }
  function chercher(pays, lon, lat) {
    for (const f of pays) for (const p of f.polys) if (dansPoly(lon, lat, p)) return f;
    return null;
  }

  // Projection d'un anneau dans des tableaux de travail ; renvoie le nombre de points visibles
  let TX = new Float64Array(4096), TY = new Float64Array(4096), TZ = new Float64Array(4096);
  function projeterAnneau(M, a) {
    if (TX.length < a.n) { TX = new Float64Array(2 * a.n); TY = new Float64Array(2 * a.n); TZ = new Float64Array(2 * a.n); }
    let vis = 0;
    const x = a.xyz;
    for (let i = 0, j = 0; i < a.n; i++, j += 3) {
      const X = x[j], Y = x[j + 1], Z = x[j + 2];
      TX[i] = M[0] * X + M[1] * Y + M[2] * Z; TY[i] = M[3] * X + M[4] * Y + M[5] * Z;
      const z = M[6] * X + M[7] * Y + M[8] * Z;
      TZ[i] = z;
      if (z > 0) vis++;
    }
    return vis;
  }
  function arcCourt(ch, cx, cy, R, a0, a1) {  // arc du bord du disque, par le plus court chemin
    let d = a1 - a0;
    while (d > Math.PI) d -= 2 * Math.PI;
    while (d < -Math.PI) d += 2 * Math.PI;
    if (Math.abs(d) > 1e-9) ch.arc(cx, cy, R, a0, a0 + d, d < 0);
  }
  function bord(p, i) {  // point où l'arête p→i passe sur le bord du disque (z = 0), ramené au cercle
    const t = TZ[p] / (TZ[p] - TZ[i]);
    const ex = TX[p] + t * (TX[i] - TX[p]), ey = TY[p] + t * (TY[i] - TY[p]), l = Math.hypot(ex, ey) || 1;
    return [ex / l, ey / l];
  }
  // Surface visible d'un anneau, à remplir avec la règle pair-impair : la partie cachée est rabattue sur le
  // bord du disque (projection radiale), ce qui donne exactement la partie visible. Si l'anneau contient le
  // point opposé au centre de la vue (anti), ce rabattement fait un tour de trop : un cercle complet l'annule.
  function remplirAnneau(ch, a, vis, cx, cy, R, anti) {
    const n = a.n;
    if (!vis) return;
    if (vis === n) {
      ch.moveTo(cx + R * TX[0], cy - R * TY[0]);
      for (let i = 1; i < n; i++) ch.lineTo(cx + R * TX[i], cy - R * TY[i]);
      ch.closePath();
      return;
    }
    let s = 0;
    while (TZ[s] <= 0) s++;
    ch.moveTo(cx + R * TX[s], cy - R * TY[s]);
    let p = s, ang = 0;
    for (let k = 1; k <= n; k++) {
      const i = (s + k) % n, zp = TZ[p], zi = TZ[i];
      if (zp > 0 && zi > 0) ch.lineTo(cx + R * TX[i], cy - R * TY[i]);
      else if (zp > 0) {  // le contour passe derrière le globe
        const e = bord(p, i);
        ch.lineTo(cx + R * e[0], cy - R * e[1]);
        ang = Math.atan2(-e[1], e[0]);
        const ai = Math.atan2(-TY[i], TX[i]);
        arcCourt(ch, cx, cy, R, ang, ai);
        ang = ai;
      } else if (zi <= 0) {
        const ai = Math.atan2(-TY[i], TX[i]);
        arcCourt(ch, cx, cy, R, ang, ai);
        ang = ai;
      } else {  // il revient sur la face visible
        const e = bord(p, i);
        arcCourt(ch, cx, cy, R, ang, Math.atan2(-e[1], e[0]));
        ch.lineTo(cx + R * TX[i], cy - R * TY[i]);
      }
      p = i;
    }
    ch.closePath();
    if (anti && dansAnneau(anti[0], anti[1], a.ll, n)) {
      ch.moveTo(cx + R, cy);
      ch.arc(cx, cy, R, 0, 2 * Math.PI);
      ch.closePath();
    }
  }
  // Contour visible d'un anneau (frontières) ou d'une ligne ouverte (méridiens, parallèles)
  function traitAnneau(ch, a, vis, cx, cy, R, ferme) {
    const n = a.n;
    if (!vis) return;
    let dessin = false;
    for (let p = 0; p < (ferme ? n : n - 1); p++) {
      const i = (p + 1) % n, zp = TZ[p], zi = TZ[i];
      if (zp > 0 && zi > 0) {
        if (!dessin) { ch.moveTo(cx + R * TX[p], cy - R * TY[p]); dessin = true; }
        ch.lineTo(cx + R * TX[i], cy - R * TY[i]);
      } else if (zp > 0) {
        const e = bord(p, i);
        if (!dessin) ch.moveTo(cx + R * TX[p], cy - R * TY[p]);
        ch.lineTo(cx + R * e[0], cy - R * e[1]);
        dessin = false;
      } else if (zi > 0) {
        const e = bord(p, i);
        ch.moveTo(cx + R * e[0], cy - R * e[1]);
        ch.lineTo(cx + R * TX[i], cy - R * TY[i]);
        dessin = true;
      } else dessin = false;
    }
  }
  function graticule() {  // méridiens et parallèles tous les 30°, en lignes ouvertes
    const lignes = [], ligne = (pts) => {
      const n = pts.length, ll = new Float64Array(2 * n), xyz = new Float64Array(3 * n);
      pts.forEach(([L, P], i) => {
        const cp = Math.cos(P * RAD);
        ll[2 * i] = L; ll[2 * i + 1] = P;
        xyz[3 * i] = cp * Math.cos(L * RAD); xyz[3 * i + 1] = cp * Math.sin(L * RAD); xyz[3 * i + 2] = Math.sin(P * RAD);
      });
      lignes.push({ n, ll, xyz });
    };
    for (let L = -180; L < 180; L += 30) { const pts = []; for (let P = -88; P <= 88; P += 4) pts.push([L, P]); ligne(pts); }
    for (let P = -60; P <= 60; P += 30) { const pts = []; for (let L = -180; L <= 180; L += 4) pts.push([L, P]); ligne(pts); }
    return lignes;
  }
  // Zoom qui montre un pays de rayon r (degrés) sur environ un tiers du rayon du globe, voisins compris
  function zoomPour(r) {
    return Math.max(1.15, Math.min(12, 0.32 / (Math.max(r || 0, 0.05) * RAD)));
  }
  // Titres d'un pays du plus au moins performant sur la séance ; sans variation connue : à la fin
  function trier(lignes) {
    return lignes.slice().sort((a, b) => (a[5] == null) - (b[5] == null) || (b[5] - a[5]) ||
      String(a[1]).localeCompare(String(b[1]), "fr"));
  }
  function vecteur(lon, lat) {
    const L = lon * RAD, P = lat * RAD, c = Math.cos(P);
    return [c * Math.cos(L), c * Math.sin(L), Math.sin(P)];
  }
  function lonlat(v) {
    return [Math.atan2(v[1], v[0]) / RAD, Math.asin(Math.max(-1, Math.min(1, v[2]))) / RAD];
  }
  function slerp(a, b, t) {  // chemin le plus court sur la sphère, de a (t = 0) à b (t = 1)
    let d = a[0] * b[0] + a[1] * b[1] + a[2] * b[2];
    if (d < -0.9999) { a = [a[0] + 0.02, a[1] + 0.02, a[2]]; d = a[0] * b[0] + a[1] * b[1] + a[2] * b[2]; }
    const w = Math.acos(Math.max(-1, Math.min(1, d)));
    if (w < 1e-6) return b.slice();
    const s = Math.sin(w), ka = Math.sin((1 - t) * w) / s, kb = Math.sin(t * w) / s;
    const v = [ka * a[0] + kb * b[0], ka * a[1] + kb * b[1], ka * a[2] + kb * b[2]], l = Math.hypot(v[0], v[1], v[2]) || 1;
    return [v[0] / l, v[1] / l, v[2] / l];
  }
  function distanceDeg(a, b) {
    return Math.acos(Math.max(-1, Math.min(1, a[0] * b[0] + a[1] * b[1] + a[2] * b[2]))) / RAD;
  }

  const MATH = { decoder, matrice, projeter, inverse, dansAnneau, chercher, projeterAnneau, remplirAnneau, traitAnneau,
    zoomPour, trier, vecteur, lonlat, slerp, distanceDeg, graticule };
  if (typeof document === "undefined") { globalThis.GlobeMath = MATH; return; }

  // ---------- page ----------

  const G = typeof D !== "undefined" && D ? D.globe : null;
  const sec = document.getElementById("sec-globe");
  if (!sec || !G || !Array.isArray(G.t) || !G.t.length) return;
  const $g = (s) => sec.querySelector(s);
  const esc = (s) => String(s == null ? "" : s).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  const fr = (x, d) => x.toLocaleString("fr-FR", { minimumFractionDigits: d, maximumFractionDigits: d });
  const pct = (x) => x == null ? "—" : (x > 0 ? "+" : "") + fr(x, 2) + " %";
  const sens = (x) => x == null ? "flat" : x > 0 ? "up" : x < 0 ? "down" : "flat";
  const dec = (p) => p >= 1000 ? 0 : p >= 10 ? 2 : p >= 1 ? 3 : 4;
  const reduit = () => matchMedia("(prefers-reduced-motion: reduce)").matches;
  const jourCourt = (iso) => new Date(iso + "T12:00:00").toLocaleDateString("fr-FR", { day: "numeric", month: "short" });
  const drapeau = (c) => /^[A-Z]{2}$/.test(c) ? String.fromCodePoint(...[...c].map((x) => 0x1F1E6 + x.charCodeAt(0) - 65)) : "";
  const TYPE = { etf: "ETF", actions: "Action", petites: "Petite cap." };
  // Clins d'œil de chaque pays (le propriétaire a cité la baguette, la pizza et le taureau), en émojis
  const DECOR = {
    FR: ["🥖", "🥐", "🧀", "🍷"], LU: ["🏰", "🏦", "🌲"], NL: ["🌷", "🚲", "🧀"], DE: ["🥨", "🍺", "🏰", "🚗"],
    IT: ["🍕", "🍝", "☕", "🛵"], ES: ["🐂", "🥘", "💃", "☀️"], GR: ["🏛️", "🫒", "⛵"], CH: ["🧀", "🍫", "⌚", "🏔️"],
    DK: ["🚲", "🧜‍♀️", "🧱"], FI: ["🧖", "🦌", "🌲", "❄️"], IE: ["☘️", "🐑", "🎻"], BE: ["🍟", "🧇", "🍫"],
    PT: ["🐟", "🌊", "🍷"], AT: ["🎻", "🏔️", "☕"], SE: ["🦌", "🌲", "❄️"], NO: ["🐟", "🏔️", "❄️"], GB: ["☕", "💂", "🌧️"],
    US: ["🗽", "🍔", "🦅", "🏈"], CA: ["🍁", "🏒", "🦫"], MX: ["🌮", "🌵", "🪅"], BR: ["⚽", "🦜", "☕", "🏖️"],
    CL: ["🍷", "🗿", "🏔️"], CO: ["☕", "💐", "🌺"], PE: ["🦙", "🏔️", "🌽"], JP: ["🍣", "🗻", "🌸", "🚄"],
    IN: ["🍛", "🐘", "🏏", "🪷"], CN: ["🐼", "🥟", "🏮", "🐉"], KR: ["🎤", "🥢", "🍜"], TW: ["🧋", "💻", "⛰️"],
    ID: ["🌋", "🏝️", "☕", "🦎"], MY: ["🌴", "🦧", "🏙️"], PH: ["🏝️", "🥭", "🐬"], TH: ["🐘", "🌶️", "🥥", "🛺"],
    HK: ["🌃", "🥟", "⛴️"], SG: ["🦁", "🌆", "🍜"], AU: ["🦘", "🐨", "🏄"], NZ: ["🥝", "🐑", "🏉"],
    CZ: ["🍺", "🏰", "🎻"], HU: ["🌶️", "♨️", "🎻"], PL: ["🥟", "🎹", "🏰"], TR: ["☕", "🧿", "🎈", "🕌"],
    SA: ["🐪", "🌴", "🏜️"], AE: ["🏙️", "⛵", "🦅"], QA: ["⚽", "🦪", "🏜️"], KW: ["🛢️", "⛵", "🏜️"],
    IL: ["🍊", "💻", "🏜️"], ZA: ["🦁", "🐧", "💎", "🍇"],
  };

  // Titres par pays, pays du plus au moins fourni
  const PAR = {};
  G.t.forEach((l) => (l[8] || []).forEach((c) => (PAR[c] = PAR[c] || []).push(l)));
  const NOMS = {};  // noms des pays sans titre, lus dans le tracé
  const nomPays = (c) => (G.p && G.p[c] ? G.p[c][0] : NOMS[c] || c);
  const CODES = Object.keys(PAR).sort((a, b) => PAR[b].length - PAR[a].length || nomPays(a).localeCompare(nomPays(b), "fr"));
  const NB = G.t.length;
  sec.hidden = false;
  $g("#globe-nb").textContent = `${NB} titres suivis dans ${CODES.length} pays`;

  // Drapeaux en émojis : absents de certains systèmes (Windows), où ils s'affichent en lettres
  const drapeauxOk = (function () {
    try {
      const c = document.createElement("canvas"); c.width = c.height = 20;
      const x = c.getContext("2d"); x.font = "16px sans-serif"; x.textBaseline = "top"; x.fillText(drapeau("FR"), 0, 0);
      const d = x.getImageData(0, 0, 20, 20).data;
      for (let i = 0; i < d.length; i += 4) if (d[i + 3] > 100 && Math.abs(d[i] - d[i + 2]) > 60) return true;
    } catch (e) { /* lecture des pixels refusée : on garde les drapeaux */ return true; }
    return false;
  })();
  if (!drapeauxOk) sec.classList.add("sans-drapeau");

  // ---------- liste des pays (aussi le moyen de choisir au clavier ou au lecteur d'écran) ----------
  const rangee = $g("#globe-pays");
  rangee.innerHTML = CODES.map((c) => `<button type="button" class="pays-chip" data-pays="${esc(c)}" aria-pressed="false">` +
    `<span class="pc-dr" aria-hidden="true">${drapeau(c)}</span>${esc(nomPays(c))}<span class="pc-nb">${PAR[c].length}</span></button>`).join("");
  rangee.addEventListener("click", (e) => {
    const b = e.target.closest("[data-pays]");
    if (b) choisir(b.dataset.pays, { voler: true, defiler: true });
  });
  const etat = $g("#globe-etat");
  const annoncer = (t) => { etat.textContent = t; };
  annoncer("Touche un pays orange pour voir ses titres");

  // ---------- fiche du pays ----------
  const fiche = $g("#pays-fiche");
  const PAS = 25;
  let choisi = null, montres = PAS, ordre = [];
  const apparition = "IntersectionObserver" in window ? new IntersectionObserver((es) => es.forEach((e) => {
    if (!e.isIntersecting) return;
    apparition.unobserve(e.target);
    e.target.classList.add("apparu");
  }), { rootMargin: "0px 0px -6% 0px" }) : null;

  function ligneTitre(l, i, max) {
    const [t, nom, cat, prix, devise, v, date, pea, codes, regle, levier] = l;
    const autres = regle === "m" ? codes.length - 1 : 0;
    const infos = [esc(t), TYPE[cat] || "", levier ? "effet de levier" : "", regle === "d" ? "fonds créé ici" : "",
      regle === "z" ? "investit ici" : "", autres ? `couvre aussi ${autres} autre${autres > 1 ? "s" : ""} pays` : ""].filter(Boolean).join(" · ");
    const ancien = date && G.date && date !== G.date ? `<em>cours du ${jourCourt(date)}</em>` : "";
    const w = v == null || !max ? 0 : Math.max(4, Math.min(100, Math.abs(v) / max * 100));
    return `<li><div class="pf-l" data-t="${esc(t)}" tabindex="0" role="button" aria-label="Fiche détaillée : ${esc(nom)}" style="--d:${Math.min(i % PAS, 10) * 35}ms">` +
      `<span class="pf-rg num">${i + 1}</span>` +
      `<span class="pf-t"><strong>${esc(nom)}</strong><small>${infos}</small>${pea === 1 ? "" : pea === 0 ? '<span class="pf-pea pf-non">Non éligible au PEA</span>' : '<span class="pf-pea">PEA à vérifier</span>'}</span>` +
      `<span class="pf-px num">${prix == null ? "—" : fr(prix, dec(prix))} <span class="dev">${esc(devise || "")}</span>${ancien}</span>` +
      `<span class="pf-v num ${sens(v)}">${pct(v)}<i class="pf-barre ${sens(v)}" style="--w:${w.toFixed(0)}%"></i></span></div></li>`;
  }
  function rendreListe() {
    const ol = $g("#pf-liste"), max = Math.max(0, ...ordre.map((l) => Math.abs(l[5] || 0)));
    const avant = ol.children.length;
    ol.insertAdjacentHTML("beforeend", ordre.slice(avant, montres).map((l, k) => ligneTitre(l, avant + k, max)).join(""));
    [...ol.children].slice(avant).forEach((li) => { const x = li.firstElementChild; if (apparition && !reduit()) apparition.observe(x); else x.classList.add("apparu"); });
    const reste = ordre.length - montres, b = $g("#pf-plus");
    b.hidden = reste <= 0;
    b.textContent = reste > PAS ? `Voir ${PAS} titres de plus (${reste} restants)` : `Voir les ${reste} derniers titres`;
  }
  function rendreFiche(c) {
    const L = PAR[c] || [], p = (G.p && G.p[c]) || [nomPays(c), ""];
    ordre = trier(L);
    montres = Math.min(PAS, ordre.length);
    const hausse = L.filter((l) => l[5] > 0).length, baisse = L.filter((l) => l[5] < 0).length;
    const connus = ordre.filter((l) => l[5] != null), haut = connus[0], bas = connus[connus.length - 1];
    const aVerifier = L.filter((l) => l[7] == null).length, nonElig = L.filter((l) => l[7] === 0).length;
    const deco = (DECOR[c] || ["🌍", "📈"]).map((e, i) => `<span style="--i:${i}">${e}</span>`).join("");
    fiche.innerHTML = `<div class="pf-mini" aria-hidden="true"><span class="pf-dr">${drapeau(c)}</span><strong>${esc(p[0])}</strong><span>${L.length} titre${L.length > 1 ? "s" : ""}</span></div>
      <header class="pf-tete"><div class="pf-fond" aria-hidden="true">${drapeau(c)}</div>
        <div class="pf-titre"><div class="kicker">${esc(p[1] || "Pays")} · ${L.length} titre${L.length > 1 ? "s" : ""} suivi${L.length > 1 ? "s" : ""}</div>
        <h3>${esc(p[0])}</h3>
        <p class="pf-deco" aria-hidden="true">${deco}</p></div></header>
      <div class="pf-stats">
        <div class="card"><div class="nom">En hausse sur la séance</div><div class="val num up">${hausse}</div></div>
        <div class="card"><div class="nom">En baisse</div><div class="val num down">${baisse}</div></div>
        ${haut && haut[5] > 0 ? `<div class="card"><div class="nom">Meilleure variation</div><div class="val num up">${pct(haut[5])}</div><div class="chg flat">${esc(haut[1])}</div></div>` : ""}
        ${bas && bas[5] < 0 ? `<div class="card"><div class="nom">Plus forte baisse</div><div class="val num down">${pct(bas[5])}</div><div class="chg flat">${esc(bas[1])}</div></div>` : ""}
      </div>
      <p class="note">Classés du plus au moins performant sur la dernière séance : l'ordre change à chaque fiche. Touche un titre pour sa fiche complète.${aVerifier ? ` ${aVerifier} titre${aVerifier > 1 ? "s" : ""} dont l'éligibilité au PEA n'est pas confirmée par deux sources : à vérifier auprès de ta banque.` : ""}${nonElig ? ` ${nonElig} titre${nonElig > 1 ? "s" : ""} non éligible${nonElig > 1 ? "s" : ""} au PEA d'après le contrôle quotidien : à retirer des titres suivis.` : ""}</p>
      <ol class="pf-liste" id="pf-liste"></ol>
      <button type="button" class="btn sec pf-plus" id="pf-plus" hidden></button>
      <p class="note">Information et apprentissage, pas un conseil en investissement : ni conseil ni recommandation.</p>`;
    fiche.hidden = false;
    rendreListe();
    $g("#pf-plus").addEventListener("click", () => { montres = Math.min(ordre.length, montres + PAS); rendreListe(); });
    majMini();
  }
  // Quand le grand titre passe sous le haut de l'écran, une petite barre collante (nom et drapeau) le
  // remplace, comme les grands titres d'iOS ; elle ne prend pas de place, donc rien ne saute.
  let attenteMini = 0;
  function majMini() {
    const m = $g(".pf-mini"), t = $g(".pf-tete");
    if (!m || !t || fiche.hidden) return;
    const bas = fiche.getBoundingClientRect().bottom;
    m.classList.toggle("visible", t.getBoundingClientRect().bottom < 56 && bas > 120);
  }
  addEventListener("scroll", () => { if (!attenteMini) attenteMini = requestAnimationFrame(() => { attenteMini = 0; majMini(); }); }, { passive: true });
  function defilerVersFiche() {
    const r = fiche.getBoundingClientRect();
    if (r.top > innerHeight * 0.8) scrollBy({ top: r.top - innerHeight * 0.12, behavior: reduit() ? "auto" : "smooth" });
  }
  function choisir(c, o) {
    o = o || {};
    if (!PAR[c]) { annoncer(`${nomPays(c)} : aucun titre suivi`); return; }
    choisi = c;
    rangee.querySelectorAll("[data-pays]").forEach((b) => b.setAttribute("aria-pressed", b.dataset.pays === c ? "true" : "false"));
    const b = rangee.querySelector(`[data-pays="${c}"]`);
    if (b && b.scrollIntoView) {
      const r = b.getBoundingClientRect(), rr = rangee.getBoundingClientRect();
      if (r.left < rr.left || r.right > rr.right) rangee.scrollTo({ left: rangee.scrollLeft + r.left - rr.left - (rr.width - r.width) / 2, behavior: reduit() ? "auto" : "smooth" });
    }
    rendreFiche(c);
    annoncer(`${nomPays(c)} : ${PAR[c].length} titre${PAR[c].length > 1 ? "s" : ""} suivi${PAR[c].length > 1 ? "s" : ""}`);
    // d'abord le globe se rapproche du pays, puis la page glisse jusqu'à sa fiche si elle est plus bas
    const ensuite = o.defiler ? defilerVersFiche : null;
    if (globe && o.voler !== false) globe.voler(c, ensuite);
    else { if (globe) globe.dessiner(); if (ensuite) ensuite(); }
  }

  // ---------- globe ----------
  let globe = null;
  const base = /\/archives\/[^/]*$/.test(location.pathname) ? "../" : "";
  const lire = (nom) => fetch(base + "globe/" + nom + "?v=1", { credentials: "same-origin" }).then((r) => {
    if (!r.ok) throw new Error("HTTP " + r.status);
    return r.json();
  });
  function charger() {
    annoncer("Chargement du globe…");
    lire("monde-110m.json").then((j) => {
      const pays = decoder(j.pays);
      pays.forEach((f) => { if (f.c && !NOMS[f.c]) NOMS[f.c] = f.n; });
      globe = Globe(pays);
      annoncer(choisi ? `${nomPays(choisi)} : ${PAR[choisi].length} titres suivis` : "Touche un pays orange pour voir ses titres · fais tourner le globe du doigt");
    }).catch(() => {
      sec.classList.add("sans-globe");
      annoncer("Globe indisponible pour le moment : la liste des pays ci-dessous reste utilisable.");
    });
  }
  if ("IntersectionObserver" in window) {
    const obs = new IntersectionObserver((es) => { if (es.some((e) => e.isIntersecting)) { obs.disconnect(); charger(); } }, { rootMargin: "700px 0px" });
    obs.observe(sec);
  } else charger();

  function Globe(pays110) {
    const canvas = $g("#globe"), boite = canvas.parentElement, ctx = canvas.getContext("2d");
    let pays = pays110, pays50 = null, charge50 = false;
    const GRILLE = graticule();
    let lon0 = -35, lat0 = 30, zoom = 1, W = 0, H = 0, dpr = 1, survol = null, anim = null, couleurs = null;
    const chaud = (c) => !!PAR[c];
    const parCode = () => { const m = {}; pays.forEach((f) => { if (f.c) m[f.c] = f; }); return m; };
    let INDEX = parCode();
    function lireCouleurs() {
      const s = getComputedStyle(sec), v = (k, d) => (s.getPropertyValue(k) || "").trim() || d;
      couleurs = { mer1: v("--g-mer1", "#8cc7f0"), mer2: v("--g-mer2", "#2a6fb0"), terre: v("--g-terre", "#8fcf8a"),
        chaud: v("--g-chaud", "#f39a33"), choisi: v("--g-choisi", "#e3650c"), trait: v("--g-trait", "rgba(255,255,255,.7)"),
        grille: v("--g-grille", "rgba(255,255,255,.2)"), halo: v("--g-halo", "rgba(80,160,230,.35)"),
        encre: v("--ink", "#1a1d1b"), fond: v("--surface", "#fffdf8"), police: getComputedStyle(document.body).fontFamily };
    }
    lireCouleurs();
    function taille() {
      const r = boite.getBoundingClientRect();
      dpr = Math.min(window.devicePixelRatio || 1, 3);
      W = Math.max(1, Math.round(r.width)); H = Math.max(1, Math.round(r.height));
      canvas.width = Math.round(W * dpr); canvas.height = Math.round(H * dpr);
      dessiner();
    }
    const geo = () => { const R0 = Math.min(W, H) / 2 - 10; return { cx: W / 2, cy: H / 2, R0, R: R0 * zoom }; };
    function demander50() {
      if (charge50) return;
      charge50 = true;
      lire("monde-50m.json").then((j) => {
        pays50 = decoder(j.pays);
        pays50.forEach((f) => { if (f.c && !NOMS[f.c]) NOMS[f.c] = f.n; });
        choisirTrace();
        dessiner();
      }).catch(() => { /* le tracé simple reste affiché */ });
    }
    function choisirTrace() {
      const p = zoom >= 2.2 && pays50 ? pays50 : pays110;
      if (p !== pays) { pays = p; INDEX = parCode(); }
    }
    // pays assez petits à l'écran pour avoir un repère touchable (Luxembourg, Singapour, Qatar…)
    function reperes(g) {
      const out = [];
      for (const c of CODES) {
        const f = INDEX[c], p = G.p[c];
        if (!p) continue;
        if (f && f.r * RAD * g.R >= 5) continue;
        out.push([c, p[3], p[2]]);
      }
      return out;
    }
    function dessiner() {
      if (!W) return;
      choisirTrace();
      lon0 = ((lon0 % 360) + 540) % 360 - 180;  // après plusieurs tours, la longitude revient entre -180 et 180
      const g = geo(), M = matrice(lon0, lat0), anti = [lon0 > 0 ? lon0 - 180 : lon0 + 180, -lat0];
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      ctx.clearRect(0, 0, W, H);
      const c = couleurs;
      // halo de l'atmosphère et océan
      if (g.R < Math.hypot(W, H)) {
        const h = ctx.createRadialGradient(g.cx, g.cy, g.R * 0.96, g.cx, g.cy, g.R * 1.06);
        h.addColorStop(0, c.halo); h.addColorStop(1, "rgba(0,0,0,0)");
        ctx.fillStyle = h; ctx.beginPath(); ctx.arc(g.cx, g.cy, g.R * 1.06, 0, 2 * Math.PI); ctx.fill();
      }
      const mer = ctx.createRadialGradient(g.cx - g.R * 0.35, g.cy - g.R * 0.4, g.R * 0.05, g.cx, g.cy, g.R);
      mer.addColorStop(0, c.mer1); mer.addColorStop(1, c.mer2);
      ctx.save();
      ctx.beginPath(); ctx.arc(g.cx, g.cy, g.R, 0, 2 * Math.PI);
      ctx.fillStyle = mer; ctx.fill(); ctx.clip();
      // ce qui peut être à l'écran : calotte de rayon `vue` autour du centre
      const s = Math.hypot(W / 2, H / 2) / g.R, vue = s >= 1 ? Math.PI / 2 : Math.asin(s);
      const V = [M[6], M[7], M[8]];
      const grille = new Path2D();
      for (const l of GRILLE) traitAnneau(grille, l, projeterAnneau(M, l), g.cx, g.cy, g.R, false);
      ctx.strokeStyle = c.grille; ctx.lineWidth = 0.8; ctx.stroke(grille);
      const terre = new Path2D(), chauds = new Path2D(), elu = new Path2D(), sous = new Path2D(), traits = new Path2D();
      for (const f of pays) {
        const ch = f.c === choisi ? elu : f.c && f.c === survol ? sous : chaud(f.c) ? chauds : terre;
        for (const p of f.polys) {
          const d = V[0] * p.c[0] + V[1] * p.c[1] + V[2] * p.c[2];
          if (d < Math.cos(Math.min(Math.PI, vue + p.rayon))) continue;
          for (const a of p.rings) {
            const vis = projeterAnneau(M, a);
            if (!vis) continue;
            remplirAnneau(ch, a, vis, g.cx, g.cy, g.R, anti);
            traitAnneau(traits, a, vis, g.cx, g.cy, g.R, true);
          }
        }
      }
      ctx.fillStyle = c.terre; ctx.fill(terre, "evenodd");
      ctx.fillStyle = c.chaud; ctx.fill(chauds, "evenodd");
      ctx.globalAlpha = 0.8; ctx.fill(sous, "evenodd"); ctx.globalAlpha = 1;
      ctx.fillStyle = c.choisi; ctx.fill(elu, "evenodd");
      ctx.strokeStyle = c.trait; ctx.lineWidth = zoom > 3 ? 1 : 0.6; ctx.stroke(traits);
      if (choisi) { ctx.lineWidth = 2; ctx.strokeStyle = c.fond; ctx.stroke(elu); }
      // relief : reflet en haut à gauche, bord plus sombre
      if (g.R < 2.2 * Math.min(W, H)) {
        const o = ctx.createRadialGradient(g.cx - g.R * 0.4, g.cy - g.R * 0.45, 0, g.cx, g.cy, g.R);
        o.addColorStop(0, "rgba(255,255,255,.16)"); o.addColorStop(0.55, "rgba(255,255,255,0)"); o.addColorStop(0.85, "rgba(0,0,0,0)"); o.addColorStop(1, "rgba(0,0,0,.22)");
        ctx.fillStyle = o; ctx.fillRect(0, 0, W, H);
      }
      ctx.restore();
      // repères des petits pays et nom du pays choisi
      for (const [code, lon, lat] of reperes(g)) {
        const q = projeter(M, lon, lat);
        if (q[2] <= 0) continue;
        const x = g.cx + g.R * q[0], y = g.cy - g.R * q[1], el = code === choisi;
        ctx.beginPath(); ctx.arc(x, y, el ? 6.5 : 4.5, 0, 2 * Math.PI);
        ctx.fillStyle = el ? c.choisi : c.chaud; ctx.fill();
        ctx.lineWidth = 1.6; ctx.strokeStyle = c.fond; ctx.stroke();
      }
      if (choisi && G.p[choisi]) {
        const q = projeter(M, G.p[choisi][3], G.p[choisi][2]);
        if (q[2] > 0.15) {
          const x = g.cx + g.R * q[0], y = g.cy - g.R * q[1], txt = nomPays(choisi);
          ctx.font = `600 13px ${c.police}`;
          const w = ctx.measureText(txt).width + 18, yy = Math.max(14, y - 26);
          ctx.fillStyle = c.fond; ctx.globalAlpha = 0.92;
          ctx.beginPath();
          if (ctx.roundRect) ctx.roundRect(x - w / 2, yy - 12, w, 24, 12); else ctx.rect(x - w / 2, yy - 12, w, 24);
          ctx.fill(); ctx.globalAlpha = 1;
          ctx.fillStyle = c.encre; ctx.textAlign = "center"; ctx.textBaseline = "middle"; ctx.fillText(txt, x, yy + 0.5);
        }
      }
    }
    let attente = 0;
    const planifier = () => { if (!attente) attente = requestAnimationFrame(() => { attente = 0; dessiner(); }); };

    // ---------- animations : arrivée, vol vers un pays, élan après un glissement ----------
    function arreter() { if (anim) { cancelAnimationFrame(anim); anim = null; } }
    function animer(duree, pas, fin) {
      arreter();
      const t0 = performance.now();
      const tour = (t) => {
        const k = Math.min(1, (t - t0) / duree);
        pas(k);
        dessiner();
        if (k < 1) anim = requestAnimationFrame(tour); else { anim = null; if (fin) fin(); }
      };
      anim = requestAnimationFrame(tour);
    }
    const doux = (t) => t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
    function vers(lon, lat, z, duree, apres) {
      const a = vecteur(lon0, lat0), b = vecteur(lon, lat), d = distanceDeg(a, b), z0 = zoom;
      if (z >= 2.2) demander50();
      if (reduit()) { lon0 = lon; lat0 = lat; zoom = z; dessiner(); if (apres) apres(); return; }
      const creux = Math.log(1 + d / 50) * 0.9;  // on s'éloigne un peu pendant les longs trajets
      animer(duree || 650 + 900 * Math.min(1, d / 120), (k) => {
        const e = doux(k), v = lonlat(slerp(a, b, e));
        lon0 = v[0]; lat0 = Math.max(-85, Math.min(85, v[1]));
        zoom = Math.max(1, Math.exp(Math.log(z0) * (1 - e) + Math.log(z) * e - creux * Math.sin(Math.PI * e)));
      }, apres);
    }
    function voler(c, apres) {
      const p = G.p[c];
      if (!p) { if (apres) apres(); return; }
      const f = (pays50 && pays50.find((x) => x.c === c)) || INDEX[c];
      vers(p[3], p[2], zoomPour(f ? f.r : 0.3), 0, apres);
    }
    function elan(vl, vp) {
      if (reduit()) return;
      let t0 = performance.now();
      arreter();
      const tour = (t) => {
        const dt = Math.min(40, t - t0); t0 = t;
        lon0 += vl * dt; lat0 = Math.max(-85, Math.min(85, lat0 + vp * dt));
        const f = Math.exp(-dt / 320); vl *= f; vp *= f;
        dessiner();
        anim = Math.abs(vl) + Math.abs(vp) > 0.0015 ? requestAnimationFrame(tour) : null;
      };
      anim = requestAnimationFrame(tour);
    }

    // ---------- toucher, souris, clavier ----------
    const pts = new Map();
    let geste = null;
    function pointe(x, y) {  // pays (ou repère) sous un point de l'écran
      const g = geo(), r = canvas.getBoundingClientRect(), px = x - r.left, py = y - r.top, M = matrice(lon0, lat0);
      for (const [code, lon, lat] of reperes(g)) {
        const q = projeter(M, lon, lat);
        if (q[2] > 0 && Math.hypot(g.cx + g.R * q[0] - px, g.cy - g.R * q[1] - py) < 16) return code;
      }
      const ll = inverse(M, (px - g.cx) / g.R, (g.cy - py) / g.R);
      if (!ll) return null;
      const f = chercher(pays, ll[0], ll[1]);
      if (f && PAR[f.c]) return f.c;
      // à côté d'un petit pays orange (Pays-Bas, Suisse… vus de loin sur un téléphone) : on le prend quand même
      let proche = null, dmin = 18;
      for (const c of CODES) {
        const p = G.p[c];
        if (!p) continue;
        const q = projeter(M, p[3], p[2]);
        const d = q[2] > 0 ? Math.hypot(g.cx + g.R * q[0] - px, g.cy - g.R * q[1] - py) : 99;
        if (d < dmin) { dmin = d; proche = c; }
      }
      if (proche) return proche;
      return f ? f.c || null : "";
    }
    function dire(code) {
      if (code === null) return annoncer("Touche un pays orange pour voir ses titres");
      if (code === "") return annoncer("Océan");
      const n = (PAR[code] || []).length;
      annoncer(n ? `${nomPays(code)} : ${n} titre${n > 1 ? "s" : ""} suivi${n > 1 ? "s" : ""} · touche pour les voir` : `${nomPays(code)} : aucun titre suivi`);
    }
    canvas.addEventListener("pointerdown", (e) => {
      if (e.pointerType === "mouse" && e.button !== 0) return;
      arreter();
      pts.set(e.pointerId, { x: e.clientX, y: e.clientY });
      try { canvas.setPointerCapture(e.pointerId); } catch (er) { /* rien */ }
      if (pts.size === 1) geste = { x0: e.clientX, y0: e.clientY, t0: performance.now(), bouge: false, v: [], deux: false };
      else if (pts.size === 2 && geste) {
        const [a, b] = [...pts.values()];
        geste.deux = true; geste.bouge = true;
        geste.d0 = Math.hypot(a.x - b.x, a.y - b.y) || 1; geste.z0 = zoom;
      }
    });
    canvas.addEventListener("pointermove", (e) => {
      if (!pts.has(e.pointerId)) {
        if (e.pointerType === "mouse" && !anim) {
          const c = pointe(e.clientX, e.clientY);
          canvas.style.cursor = c && PAR[c] ? "pointer" : "grab";
          if (c !== survol) { survol = c && PAR[c] ? c : null; dire(c); planifier(); }
        }
        return;
      }
      const avant = pts.get(e.pointerId), g = geo();
      if (pts.size === 1) {
        const dx = e.clientX - avant.x, dy = e.clientY - avant.y;
        if (Math.hypot(e.clientX - geste.x0, e.clientY - geste.y0) > 6) geste.bouge = true;
        if (geste.bouge) {
          lon0 -= dx / g.R / RAD; lat0 = Math.max(-85, Math.min(85, lat0 + dy / g.R / RAD));
          const t = performance.now();
          geste.v.push([t, -dx / g.R / RAD, dy / g.R / RAD]);
          while (geste.v.length && t - geste.v[0][0] > 90) geste.v.shift();
          planifier();
        }
      }
      pts.set(e.pointerId, { x: e.clientX, y: e.clientY });
      if (pts.size === 2 && geste && geste.deux) {
        const [a, b] = [...pts.values()], d = Math.hypot(a.x - b.x, a.y - b.y) || 1;
        zoom = Math.max(1, Math.min(16, geste.z0 * d / geste.d0));
        if (zoom >= 2.2) demander50();
        lon0 -= (e.clientX - avant.x) / 2 / g.R / RAD; lat0 = Math.max(-85, Math.min(85, lat0 + (e.clientY - avant.y) / 2 / g.R / RAD));
        planifier();
      }
    });
    function fin(e) {
      if (!pts.has(e.pointerId)) return;
      pts.delete(e.pointerId);
      if (pts.size || !geste) return;
      const g = geste;
      geste = null;
      if (e.type === "pointercancel") return;  // le navigateur a repris la main (défilement de la page)
      if (!g.bouge && performance.now() - g.t0 < 600) {
        const c = pointe(e.clientX, e.clientY);
        if (c && PAR[c]) choisir(c, { voler: true, defiler: true });
        else dire(c);
        return;
      }
      if (!g.deux && g.v.length > 1) {
        const a = g.v[0], b = g.v[g.v.length - 1], dt = Math.max(16, b[0] - a[0]);
        const sl = g.v.reduce((s, x) => s + x[1], 0) - a[1], sp = g.v.reduce((s, x) => s + x[2], 0) - a[2];
        elan(sl / dt, sp / dt);
      }
    }
    canvas.addEventListener("pointerup", fin);
    canvas.addEventListener("pointercancel", fin);
    canvas.addEventListener("pointerleave", (e) => { if (e.pointerType === "mouse" && survol) { survol = null; planifier(); } });
    // pincer sur le pavé tactile (Ctrl + molette) ou dans Safari (gestes) ; la molette seule fait défiler la page
    canvas.addEventListener("wheel", (e) => {
      if (!e.ctrlKey) return;
      e.preventDefault(); arreter();
      zoom = Math.max(1, Math.min(16, zoom * Math.exp(-e.deltaY * 0.01)));
      if (zoom >= 2.2) demander50();
      planifier();
    }, { passive: false });
    let z0g = 1;
    canvas.addEventListener("gesturestart", (e) => { e.preventDefault(); z0g = zoom; });
    canvas.addEventListener("gesturechange", (e) => {
      e.preventDefault();
      zoom = Math.max(1, Math.min(16, z0g * e.scale));
      if (zoom >= 2.2) demander50();
      planifier();
    });
    canvas.addEventListener("keydown", (e) => {
      const pas = 12 / zoom, k = e.key;
      if (k === "ArrowLeft") lon0 -= pas; else if (k === "ArrowRight") lon0 += pas;
      else if (k === "ArrowUp") lat0 = Math.min(85, lat0 + pas); else if (k === "ArrowDown") lat0 = Math.max(-85, lat0 - pas);
      else if (k === "+" || k === "=") zoom = Math.min(16, zoom * 1.4); else if (k === "-") zoom = Math.max(1, zoom / 1.4);
      else return;
      e.preventDefault(); arreter();
      if (zoom >= 2.2) demander50();
      planifier();
    });
    $g("#globe-plus").addEventListener("click", () => { const z = Math.min(16, zoom * 1.6); vers(lon0, lat0, z, 350); });
    $g("#globe-moins").addEventListener("click", () => { const z = Math.max(1, zoom / 1.6); vers(lon0, lat0, z, 350); });
    $g("#globe-europe").addEventListener("click", () => vers(12, 44, 1.25));

    if ("ResizeObserver" in window) new ResizeObserver(taille).observe(boite);
    else addEventListener("resize", taille);
    const schema = matchMedia("(prefers-color-scheme: dark)");
    const recolorer = () => { lireCouleurs(); dessiner(); };
    if (schema.addEventListener) schema.addEventListener("change", recolorer);
    new MutationObserver(recolorer).observe(document.documentElement, { attributes: true, attributeFilter: ["data-theme"] });
    taille();
    sec.classList.add("globe-pret");
    // arrivée : le globe tourne de l'Atlantique jusqu'à l'Europe
    if (reduit()) { lon0 = 12; lat0 = 44; zoom = 1.25; dessiner(); }
    else vers(12, 44, 1.25, 1500);
    return { voler, dessiner };
  }
})();
