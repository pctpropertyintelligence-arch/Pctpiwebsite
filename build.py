#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Static site generator for PCT Property Intelligence — Phase 1.

Plain HTML/CSS/JS output (no build step required to host it). This script
exists only to keep ~20 pages consistent (shared header/nav/footer/meta/
schema) while authoring; the OUTPUT is what gets deployed/zipped, not this
script.
"""
import os
import re

ROOT = os.path.dirname(os.path.abspath(__file__))
DOMAIN = "https://pctpropertyintelligence.co.uk"
BUSINESS_EMAIL = "info@pctpropertyintelligence.co.uk"
SERVICE_AREA = "Worcestershire and surrounding areas"

# --------------------------------------------------------------------------
# Icons (24x24, stroke-based line icons — no external icon library)
# --------------------------------------------------------------------------
ICONS = {
    "bolt": '<path d="M13 2 4 14h6l-1 8 9-12h-6l1-8Z" stroke-linejoin="round"/>',
    "home": '<path d="M4 11.5 12 4l8 7.5" /><path d="M6 10v9a1 1 0 0 0 1 1h4v-6h2v6h4a1 1 0 0 0 1-1v-9"/>',
    "drone": '<circle cx="12" cy="12" r="2.4"/><path d="M9.8 9.8 5 5M14.2 9.8 19 5M9.8 14.2 5 19M14.2 14.2 19 19"/><circle cx="5" cy="5" r="2"/><circle cx="19" cy="5" r="2"/><circle cx="5" cy="19" r="2"/><circle cx="19" cy="19" r="2"/>',
    "roof": '<path d="M3 12 12 4l9 8"/><path d="M5 11v8h14v-8"/><path d="M9 19v-5h6v5"/>',
    "droplet": '<path d="M12 3s6.5 7.1 6.5 11.5a6.5 6.5 0 1 1-13 0C5.5 10.1 12 3 12 3Z"/>',
    "camera": '<path d="M4 8h3.2l1.2-2h7.2l1.2 2H20a1 1 0 0 1 1 1v9a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1V9a1 1 0 0 1 1-1Z"/><circle cx="12" cy="13.5" r="3.4"/>',
    "document": '<path d="M7 2.8h7.2L19 7.6V21a.9.9 0 0 1-.9.9H7A.9.9 0 0 1 6.1 21V3.7A.9.9 0 0 1 7 2.8Z"/><path d="M14 2.8V8h5"/><path d="M9 13h6M9 16.5h6M9 9.5h2"/>',
    "map-pin": '<path d="M12 21.5S5 15 5 9.8a7 7 0 1 1 14 0c0 5.2-7 11.7-7 11.7Z"/><circle cx="12" cy="9.8" r="2.6"/>',
    "shield-check": '<path d="M12 3.2 19.5 6v6.2c0 4.9-3.3 8-7.5 9.6-4.2-1.6-7.5-4.7-7.5-9.6V6L12 3.2Z"/><path d="m9 12.2 2.1 2.1L15.3 10"/>',
    "chart": '<path d="M4 20V10M10 20V4M16 20v-7M22 20H2"/>',
    "user": '<circle cx="12" cy="8.2" r="3.4"/><path d="M4.8 20.2a7.2 7.2 0 0 1 14.4 0"/>',
    "chevron-down": '<path d="m6 9 6 6 6-6"/>',
    "chevron-right": '<path d="m9 6 6 6-6 6"/>',
    "menu": '<path d="M3.5 6.5h17M3.5 12h17M3.5 17.5h17"/>',
    "close": '<path d="m5 5 14 14M19 5 5 19"/>',
    "mail": '<path d="M3.5 5.5h17v13h-17z"/><path d="m3.8 6 8.2 6.6L20.2 6"/>',
    "phone": '<path d="M6.5 3.5 9 6l-1.7 3A12 12 0 0 0 15 16.7l3-1.7 2.5 2.5-1.4 2.6a2 2 0 0 1-2 1C9.4 20.5 3.5 14.6 3 8a2 2 0 0 1 1-2Z"/>',
    "upload": '<path d="M12 16V4M8 8l4-4 4 4"/><path d="M4 15v3.5A1.5 1.5 0 0 0 5.5 20h13a1.5 1.5 0 0 0 1.5-1.5V15"/>',
    "arrow-right": '<path d="M4 12h16M14 6l6 6-6 6"/>',
    "building": '<rect x="5" y="3.5" width="14" height="17" rx="1"/><path d="M9 8h1.2M14 8h1.2M9 12h1.2M14 12h1.2M9 16h1.2M14 16h1.2"/><path d="M10 20.5V17h4v3.5"/>',
    "clipboard": '<rect x="5.5" y="4" width="13" height="17" rx="1.2"/><path d="M9 4V3a1 1 0 0 1 1-1h4a1 1 0 0 1 1 1v1"/><path d="m8.8 12.5 2 2 4.2-4.4"/>',
    "layers": '<path d="m12 3 9 5-9 5-9-5 9-5Z"/><path d="m3 13 9 5 9-5"/>',
    "grid": '<rect x="3.5" y="3.5" width="7" height="7" rx="1"/><rect x="13.5" y="3.5" width="7" height="7" rx="1"/><rect x="3.5" y="13.5" width="7" height="7" rx="1"/><rect x="13.5" y="13.5" width="7" height="7" rx="1"/>',
    "calendar": '<rect x="3.5" y="5" width="17" height="15.5" rx="1.5"/><path d="M3.5 9.5h17M8 3v4M16 3v4"/>',
    "history": '<path d="M4 12a8 8 0 1 0 2.6-5.9"/><path d="M3.5 4v4h4"/><path d="M12 8v4.5l3 2"/>',
    "compass": '<circle cx="12" cy="12" r="9"/><path d="m15 9-4.5 1.5L9 15l4.5-1.5L15 9Z"/>',
    "check": '<path d="m5 13 4 4 10-10"/>',
    "lock": '<rect x="5" y="10.5" width="14" height="10" rx="1.5"/><path d="M8 10.5V7a4 4 0 0 1 8 0v3.5"/>',
    "cookie": '<circle cx="12" cy="12" r="9"/><circle cx="9" cy="10" r="1"/><circle cx="14" cy="8.5" r="1"/><circle cx="15" cy="14" r="1"/><circle cx="9.5" cy="15" r="1"/>',
    "wrench": '<path d="M14.7 6.3a4 4 0 0 0-5.4 5L4 16.6 7.4 20l5.3-5.3a4 4 0 0 0 5-5.4l-2.9 2.9-2.6-.6-.6-2.6 2.9-2.9Z"/>',
    "leaf": '<path d="M20 4S8.5 3 5 9.5C2 15 5 20 5 20s5 3 10.5 0C22 15.5 20 4 20 4Z"/><path d="M5 20 15 9"/>',
    "quote": '<path d="M9 7.5H5.5A1.5 1.5 0 0 0 4 9v3.5A1.5 1.5 0 0 0 5.5 14H8a1 1 0 0 1 1 1v1a2.5 2.5 0 0 1-2.5 2.5"/><path d="M18.5 7.5H15A1.5 1.5 0 0 0 13.5 9v3.5A1.5 1.5 0 0 0 15 14h2.5a1 1 0 0 1 1 1v1a2.5 2.5 0 0 1-2.5 2.5"/>',
}


def icon(name, size=22, cls=""):
    body = ICONS.get(name, ICONS["check"])
    cls_attr = ' class="%s"' % cls if cls else ""
    return (
        '<svg%s width="%d" height="%d" viewBox="0 0 24 24" fill="none" '
        'stroke="currentColor" stroke-width="1.7" stroke-linecap="round" '
        'aria-hidden="true">%s</svg>' % (cls_attr, size, size, body)
    )


# --------------------------------------------------------------------------
# Placeholder image block generator (used where no photograph exists yet)
# --------------------------------------------------------------------------
def ph(label, icon_name="camera", variant="hero", extra_class=""):
    return (
        '<div class="ph ph-%s %s" role="img" aria-label="%s">'
        '<div class="ph-inner">%s<span>%s</span></div></div>'
    ) % (variant, extra_class, label.replace('"', "'"), icon(icon_name, 26), label)


# --------------------------------------------------------------------------
# Photography. Web copies live in assets/img, built by tools/process-images.ps1
# as <key>-800.jpg and <key>-1600.jpg (hero also has -900/-2400).
# --------------------------------------------------------------------------
PHOTOS = {
    # key: (width, height) of the 1600px version
    "hero-drone-house": (1600, 905),
    "car-cottage": (1600, 905),
    "epc-loft-insulation": (1600, 905),
    "drone-pilot": (1600, 905),
    "aerial-village": (1600, 905),
    "hot-water-cylinder": (1600, 905),
    "aerial-house-real": (1600, 1200),
    "roof-moss-closeup": (1600, 1200),
    "roof-gutter-edge": (1600, 1200),
    "gutter-blocked": (1600, 1200),
    "roof-broken-tile": (1600, 1200),
    "gutter-debris": (1600, 1200),
}


def photo(prefix, key, alt, cls="", sizes="(max-width: 860px) 100vw, 50vw", eager=False):
    w, h = PHOTOS[key]
    base = "%sassets/img/%s" % (prefix, key)
    return (
        '<img class="photo %s" src="%s-800.jpg" srcset="%s-800.jpg 800w, %s-1600.jpg 1600w" '
        'sizes="%s" width="%d" height="%d" alt="%s" %s>'
    ) % (cls, base, base, base, sizes, w, h, alt.replace('"', "'"),
         'fetchpriority="high"' if eager else 'loading="lazy" decoding="async"')


ABBE_BADGE = '<img class="abbe-badge" src="{prefix}assets/img/abbe-qualified.png" width="403" height="150" alt="ABBE Qualified">'


# --------------------------------------------------------------------------
# Service catalogue (single source of truth used across nav, homepage,
# services overview, footer and each service page)
# --------------------------------------------------------------------------
SERVICES = [
    {
        "slug": "energy-assessment-epc",
        "seo_title": "EPCs & Domestic Energy Assessments in Worcestershire",
        "meta": "Need an EPC in Worcestershire? ABBE-qualified Domestic Energy Assessor for sales, lettings and homeowners, with clear advice on improving your rating.",
        "name": "Domestic Energy Assessment & EPC",
        "short": "Domestic Energy Assessment / EPC",
        "category": "Energy & Retrofit",
        "icon": "bolt",
        "status": "available",
        "image": "epc-loft-insulation", "detail": ("hot-water-cylinder", "Assessor recording hot water cylinder details during an energy assessment"),
        "alt": "Energy assessor measuring loft insulation depth in a stone cottage",
        "summary": "Domestic Energy Assessments and EPCs from an ABBE-qualified assessor, explained clearly.",
        "teaser": "EPCs and domestic energy assessments from an ABBE-qualified Domestic Energy Assessor — available now.",
    },
    {
        "slug": "retrofit-assessment",
        "seo_title": "Retrofit Assessment in Worcestershire (Coming Soon)",
        "meta": "Retrofit assessment for Worcestershire homes is coming soon from PCT Property Intelligence. EPCs are available now from our ABBE-qualified assessor.",
        "name": "Retrofit Assessment",
        "short": "Retrofit Assessment",
        "category": "Energy & Retrofit",
        "icon": "leaf",
        "status": "soon",
        "image": None,
        "summary": "Retrofit assessment and property information to support future energy improvements.",
        "teaser": "Retrofit assessment services — launching alongside our Retrofit Assessor qualification in 2026.",
    },
    {
        "slug": "drone-inspection",
        "seo_title": "Drone Roof Inspections & Surveys in Worcestershire",
        "meta": "CAA-registered drone roof and building inspections across Worcestershire. See roofs, chimneys and gutters clearly without scaffolding, with photos and notes.",
        "name": "Drone Inspection",
        "short": "Drone Inspection",
        "category": "Drone & Visual Inspection",
        "icon": "drone",
        "status": "available",
        "image": "drone-pilot", "detail": ("aerial-house-real", "Drone photograph of a house, roof and garden captured by PCT"),
        "alt": "Drone pilot in hi-vis flying an inspection drone beside a Cotswold stone house",
        "summary": "CAA-registered aerial inspection of roofs, buildings, gutters and difficult-to-access areas.",
        "teaser": "Aerial visual inspection using a CAA-registered drone and pilot — available now.",
    },
    {
        "slug": "roof-inspection",
        "seo_title": "Roof Inspections in Worcestershire",
        "meta": "Visual roof inspections in Worcestershire combining ground-level and drone views. Cracked or slipped tiles, moss and flashing issues documented with clear photos.",
        "name": "Roof Inspection",
        "short": "Roof Inspection",
        "category": "Roof & External",
        "icon": "roof",
        "status": "available",
        "image": "roof-moss-closeup", "detail": ("roof-broken-tile", "Drone photograph showing a cracked roof tile next to a gutter"),
        "alt": "Close-up of concrete roof tiles with heavy moss growth, photographed during an inspection",
        "summary": "Ground-level and aerial visual inspection of roofs, with clear photographic evidence.",
        "teaser": "Visual roof inspection combining ground-level and aerial techniques — available now.",
    },
    {
        "slug": "gutter-inspection-cleaning",
        "seo_title": "Gutter Inspections in Worcestershire",
        "meta": "Gutter and downpipe inspections across Worcestershire, from the ground and the air. Blockages, moss and overflow risks photographed. Gutter cleaning coming soon.",
        "name": "Gutter Inspection & Cleaning",
        "short": "Gutter Inspection & Cleaning",
        "category": "Roof & External",
        "icon": "droplet",
        "status": "available",
        # Inspection is live; cleaning equipment not yet purchased.
        "badges": [("available", "Inspection available"), ("soon", "Cleaning coming soon")],
        "image": "gutter-blocked", "detail": ("gutter-debris", "Gutter run clogged with moss debris, photographed from above"),
        "alt": "Aerial view of a gutter holding standing water and moss debris beside a tiled roof",
        "summary": "Photographic inspection of gutters and downpipes, available now. Gutter cleaning is coming soon.",
        "teaser": "Gutter inspection available now; gutter cleaning coming soon.",
    },
    {
        "slug": "property-documentation",
        "seo_title": "Property Condition Records in Worcestershire",
        "meta": "Structured property condition records for landlords, property managers and homeowners in Worcestershire: organised photographs and a clear written summary.",
        "name": "Property Documentation",
        "short": "Property Documentation",
        "category": "Property Intelligence",
        "icon": "document",
        "status": "available",
        "image": "hot-water-cylinder", "detail": ("roof-gutter-edge", "Close-up of moss along a gutter edge below concrete roof tiles"),
        "alt": "Inspector recording readings from a hot water cylinder on a clipboard",
        "summary": "Structured reports, photographs and property information you can keep on file.",
        "teaser": "Professional documentation of your property's condition — available now.",
    },
    {
        "slug": "photography-visual-records",
        "seo_title": "Property & Aerial Drone Photography in Worcestershire",
        "meta": "Property and aerial drone photography in Worcestershire for sales, lettings, insurance and before/after records. High-resolution images, clearly organised.",
        "name": "Photography & Visual Property Records",
        "short": "Photography / Visual Property Records",
        "category": "Property Intelligence",
        "icon": "camera",
        "status": "available",
        "image": "aerial-house-real", "detail": ("aerial-village", "Aerial view of a Cotswold stone house and neighbouring village roofs"),
        "alt": "Aerial photograph of a semi-detached house, garden and driveway captured by drone",
        "summary": "Professional photographic and visual records — including before/after documentation.",
        "teaser": "Clear, professional photographic records of your property — available now.",
    },
]

CATEGORY_ORDER = [
    "Property Intelligence",
    "Energy & Retrofit",
    "Drone & Visual Inspection",
    "Roof & External",
]

RESOURCES = [
    {
        "slug": "how-often-should-gutters-be-cleaned",
        "title": "How often should gutters be cleaned?",
        "tag": "Roof & Gutter",
        "icon": "droplet",
        "image": "gutter-debris",
        "alt": "Gutter run clogged with moss and debris, photographed from above",
        "summary": "A practical guide to gutter cleaning frequency, warning signs of blockages, and why regular inspection matters.",
    },
    {
        "slug": "what-can-a-drone-roof-inspection-identify",
        "title": "What can a drone roof inspection identify?",
        "tag": "Drone & Visual Inspection",
        "icon": "drone",
        "image": "roof-broken-tile",
        "alt": "Drone photograph showing a cracked roof tile and moss beside a gutter",
        "summary": "What aerial visual inspection can and can't tell you about your roof — and how it fits alongside other checks.",
    },
    {
        "slug": "what-is-a-property-inspection",
        "title": "What is a property inspection?",
        "tag": "Property Intelligence",
        "icon": "document",
        "image": "aerial-village",
        "alt": "Aerial view of a Cotswold stone house and neighbouring village roofs",
        "summary": "An introduction to property inspection and documentation, and what to expect from a visit.",
    },
]

NAV_SECONDARY = [
    ("About PCT", "about.html"),
    ("Resources", "resources.html"),
    ("Contact", "contact.html"),
]

# --------------------------------------------------------------------------
# HTML shell helpers
# --------------------------------------------------------------------------
GA_STUB = """
    <!-- Analytics (Phase 1 foundation) -->
    <!--
      No tracking runs until the visitor accepts analytics cookies (see
      assets/js/main.js). Replace G-XXXXXXXXXX with the real GA4 Measurement
      ID before launch, then uncomment the loader lines below.
    -->
    <script>
      window.pctEnableAnalytics = function () {
        /*
        var s = document.createElement('script');
        s.async = true;
        s.src = 'https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX';
        document.head.appendChild(s);
        window.dataLayer = window.dataLayer || [];
        function gtag(){dataLayer.push(arguments);}
        gtag('js', new Date());
        gtag('config', 'G-XXXXXXXXXX', { anonymize_ip: true });
        */
      };
    </script>
""".strip("\n")


def nav_dropdown():
    cats = {}
    for s in SERVICES:
        cats.setdefault(s["category"], []).append(s)
    panel = ""
    for cat in CATEGORY_ORDER:
        panel += '<div class="dropdown-cat-label">%s</div>' % cat
        for s in cats[cat]:
            panel += (
                '<a class="dropdown-link" href="{prefix}services/{slug}.html">'
                '<span class="icon-wrap">{icon}</span>'
                "<span><strong>{name}</strong><span>{summary}</span></span></a>"
            ).format(prefix="{prefix}", slug=s["slug"], icon=icon(s["icon"], 17), name=s["short"], summary=s["summary"])
    return panel


NAV_DROPDOWN_TEMPLATE = nav_dropdown()


def brand_html(prefix):
    # Lock-up built from the client's own logo artwork (PCT mark) + wordmark text.
    return (
        '<a class="brand" href="{p}index.html" aria-label="PCT Property Intelligence home">'
        '<img class="brand-logo" src="{p}assets/img/logo-mark-dark.png" width="303" height="160" alt="PCT">'
        '<span class="brand-text"><span class="brand-name">Property Intelligence</span>'
        '<span class="brand-tag">Survey<i>.</i> Assess<i>.</i> Certify<i>.</i></span></span></a>'
    ).format(p=prefix)


def header_html(prefix, active=""):
    dropdown = NAV_DROPDOWN_TEMPLATE.format(prefix=prefix)

    def cur(key):
        return ' aria-current="page"' if active == key else ""

    return """
<a class="skip-link" href="#main">Skip to main content</a>
<header class="site-header">
  <div class="container header-inner">
    {brand}
    <nav class="main-nav" data-main-nav aria-label="Primary">
      <ul>
        <li><a class="nav-link" href="{prefix}index.html"{cur_home}>Home</a></li>
        <li class="nav-item-dropdown">
          <a class="nav-link" href="{prefix}services.html"{cur_services}>Services {chev}</a>
          <div class="dropdown-panel">{dropdown}</div>
        </li>
        <li><a class="nav-link" href="{prefix}about.html"{cur_about}>About PCT</a></li>
        <li><a class="nav-link" href="{prefix}resources.html"{cur_resources}>Resources</a></li>
        <li><a class="nav-link" href="{prefix}contact.html"{cur_contact}>Contact</a></li>
      </ul>
      <div class="header-actions-mobile">
        <a class="btn btn-primary btn-block" href="{prefix}contact.html">Request an Assessment</a>
        <a class="btn btn-secondary btn-block" href="{prefix}portal.html">Client Portal</a>
      </div>
    </nav>
    <div class="header-actions">
      <a class="header-link" href="{prefix}portal.html">{user} Client Portal</a>
      <a class="btn btn-primary" href="{prefix}contact.html">Request an Assessment</a>
    </div>
    <button class="nav-toggle" data-nav-toggle aria-label="Open menu" aria-expanded="false">{menu}</button>
  </div>
</header>
""".format(
        prefix=prefix,
        brand=brand_html(prefix),
        user=icon("user", 16),
        chev='<svg class="dropdown-caret" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" aria-hidden="true">' + ICONS["chevron-down"] + "</svg>",
        dropdown=dropdown,
        menu=icon("menu", 18),
        cur_home=cur("home"),
        cur_services=cur("services"),
        cur_about=cur("about"),
        cur_resources=cur("resources"),
        cur_contact=cur("contact"),
    )


def footer_html(prefix):
    service_links = "".join(
        '<li><a href="{p}services/{slug}.html">{name}</a></li>'.format(p=prefix, slug=s["slug"], name=s["short"])
        for s in SERVICES
    )
    return """
<footer class="site-footer">
  <div class="container">
    <div class="footer-top">
      <div class="footer-brand">
        <a href="{prefix}index.html" aria-label="PCT Property Intelligence home">
          <img class="footer-logo" src="{prefix}assets/img/logo-full-dark.png" width="468" height="360" alt="PCT Property Intelligence &ndash; Survey. Assess. Certify." loading="lazy">
        </a>
        <p>Property inspection, energy assessment and visual records for homeowners, landlords and property professionals across {area}.</p>
        <div class="footer-credentials">
          <span class="footer-badge">{abbe}</span>
          <span class="pill">ABBE-qualified Domestic Energy Assessor</span>
          <span class="pill">CAA-registered drone operator</span>
        </div>
      </div>
      <div class="footer-col">
        <h4>Services</h4>
        <ul>{service_links}<li><a href="{prefix}services.html">All services</a></li></ul>
      </div>
      <div class="footer-col">
        <h4>Company</h4>
        <ul>
          <li><a href="{prefix}about.html">About PCT</a></li>
          <li><a href="{prefix}resources.html">Resources</a></li>
          <li><a href="{prefix}contact.html">Contact</a></li>
          <li><a href="{prefix}portal.html">Client Portal</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h4>Get in touch</h4>
        <ul>
          <li><a href="mailto:{email}">{email}</a></li>
          <li><span>{area}</span></li>
          <li><a href="{prefix}contact.html">Request an assessment</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <span>&copy; <span data-year></span> PCT Property Intelligence. All rights reserved.</span>
      <div class="footer-bottom-links">
        <a href="{prefix}privacy-policy.html">Privacy Policy</a>
        <a href="{prefix}terms.html">Terms</a>
        <a href="{prefix}cookie-policy.html">Cookie Policy</a>
      </div>
    </div>
  </div>
</footer>

<div class="cookie-banner" data-cookie-banner role="dialog" aria-live="polite" aria-label="Cookie notice">
  <p>We use essential cookies to run this site, and optional analytics cookies to understand how it's used. See our <a href="{prefix}cookie-policy.html" style="text-decoration:underline;">Cookie Policy</a> for details.</p>
  <div class="cta-row">
    <button class="btn btn-primary" data-cookie-accept>Accept analytics</button>
    <button class="btn btn-secondary" data-cookie-decline>Essential only</button>
  </div>
</div>
""".format(prefix=prefix, abbe=ABBE_BADGE.format(prefix=prefix).replace("<img ", '<img loading="lazy" '),
           area=SERVICE_AREA, email=BUSINESS_EMAIL, service_links=service_links)


def page(
    slug,
    title,
    description,
    content,
    prefix="",
    active="",
    body_class="",
    schema="",
    og_type="website",
    seo_title=None,
    robots="index, follow",
    head_extra="",
    og_image="hero-drone-house",
):
    # seo_title: keyword-led <title> for search results (defaults to the page title)
    canonical = DOMAIN + "/" + (slug if slug != "index" else "")
    full_title = (seo_title or title) + " | PCT Property Intelligence"
    og_w, og_h = PHOTOS[og_image]
    return """<!DOCTYPE html>
<html lang="en-GB">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<script>document.documentElement.classList.add('js')</script>
<title>{full_title}</title>
<meta name="description" content="{description}">
<link rel="canonical" href="{canonical}">
<meta name="robots" content="{robots}">
<meta name="theme-color" content="#0B1F33">

<meta property="og:type" content="{og_type}">
<meta property="og:locale" content="en_GB">
<meta property="og:site_name" content="PCT Property Intelligence">
<meta property="og:title" content="{full_title}">
<meta property="og:description" content="{description}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{domain}/assets/img/{og_image}-1600.jpg">
<meta property="og:image:width" content="{og_w}">
<meta property="og:image:height" content="{og_h}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{full_title}">
<meta name="twitter:description" content="{description}">
<meta name="twitter:image" content="{domain}/assets/img/{og_image}-1600.jpg">

<link rel="icon" type="image/svg+xml" href="{prefix}assets/img/favicon.svg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Montserrat:wght@600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{prefix}assets/css/style.css">
{head_extra}
{schema}
{ga}
</head>
<body class="{body_class}">
{header}
<main id="main">
{content}
</main>
{footer}
<script src="{prefix}assets/js/main.js" defer></script>
</body>
</html>
""".format(
        full_title=full_title,
        description=description,
        robots=robots,
        head_extra=head_extra,
        og_image=og_image, og_w=og_w, og_h=og_h,
        canonical=canonical,
        domain=DOMAIN,
        og_type=og_type,
        prefix=prefix,
        schema=schema,
        ga=GA_STUB,
        body_class=body_class,
        header=header_html(prefix, active),
        content=content,
        footer=footer_html(prefix),
    )


def write(path, html):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(html)
    print("wrote", path)


def status_badge(status, label=None):
    if status == "available":
        return '<span class="badge badge-available"><span class="badge-dot"></span>%s</span>' % (label or "Available now")
    return '<span class="badge badge-soon"><span class="badge-dot"></span>%s</span>' % (label or "Coming soon")


def service_badges(s):
    """One badge normally; services with partly-available scope list each part."""
    if s.get("badges"):
        return '<span class="badge-group">%s</span>' % "".join(status_badge(st, lb) for st, lb in s["badges"])
    return status_badge(s["status"])
