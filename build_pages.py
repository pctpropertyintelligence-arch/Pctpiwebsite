#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Content for every Phase 1 page. Run: python3 build_pages.py"""
from build import (
    ROOT, DOMAIN, BUSINESS_EMAIL, SERVICE_AREA, SERVICES, CATEGORY_ORDER,
    RESOURCES, ABBE_BADGE, icon, ph, photo, page, write, status_badge, service_badges,
)
import json
import os

# --------------------------------------------------------------------------
# Shared fragments
# --------------------------------------------------------------------------

def schema_tag(data):
    return '<script type="application/ld+json">%s</script>' % json.dumps(data, indent=None)


BUSINESS_ID = DOMAIN + "/#business"
AREA_SERVED = {"@type": "AdministrativeArea", "name": "Worcestershire", "containedInPlace": {"@type": "Country", "name": "United Kingdom"}}

# Sitewide business entity. Add "telephone" and "address" here once they are
# published, and "sameAs" with the Google Business Profile / social URLs.
LOCAL_BUSINESS_SCHEMA = schema_tag({
    "@context": "https://schema.org",
    "@graph": [
        {
            "@type": "ProfessionalService",
            "@id": BUSINESS_ID,
            "name": "PCT Property Intelligence",
            "alternateName": "PCTPI",
            "slogan": "Survey. Assess. Certify.",
            "url": DOMAIN + "/",
            "email": BUSINESS_EMAIL,
            "logo": DOMAIN + "/assets/img/logo-full-light.png",
            "image": DOMAIN + "/assets/img/hero-drone-house-1600.jpg",
            "areaServed": AREA_SERVED,
            "description": "EPCs from an ABBE-qualified Domestic Energy Assessor, CAA-registered drone roof inspections, roof and gutter inspections, and clear photographic property records across Worcestershire.",
            "knowsAbout": ["Energy Performance Certificates", "Domestic Energy Assessment", "Drone roof inspection",
                           "Roof inspection", "Gutter inspection", "Property condition records", "Aerial photography"],
            "hasCredential": {
                "@type": "EducationalOccupationalCredential",
                "name": "ABBE Domestic Energy Assessor qualification",
                "credentialCategory": "qualification",
                "recognizedBy": {"@type": "Organization", "name": "ABBE (Awarding Body for the Built Environment)"},
            },
            "hasOfferCatalog": {
                "@type": "OfferCatalog",
                "name": "Property services",
                "itemListElement": [
                    {"@type": "Offer", "itemOffered": {"@type": "Service", "name": s["name"],
                                                       "url": "%s/services/%s.html" % (DOMAIN, s["slug"])}}
                    for s in SERVICES if s["status"] == "available"
                ],
            },
        },
        {
            "@type": "WebSite",
            "@id": DOMAIN + "/#website",
            "url": DOMAIN + "/",
            "name": "PCT Property Intelligence",
            "inLanguage": "en-GB",
            "publisher": {"@id": BUSINESS_ID},
        },
    ],
})


def breadcrumb_schema(items):
    """items: list of (label, path) where path is relative to the site root ('' = home)."""
    return {
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": label, "item": "%s/%s" % (DOMAIN, path)}
            for i, (label, path) in enumerate(items)
        ],
    }


def strip_tags(html):
    import re
    return re.sub(r"<[^>]+>", "", html).replace("&mdash;", "—").replace("&ndash;", "–").replace("&amp;", "&").replace('\\"', '"')


def breadcrumb(prefix, items):
    """items: list of (label, href|None)"""
    parts = []
    for label, href in items:
        if href:
            parts.append('<a href="%s%s">%s</a>' % (prefix, href, label))
        else:
            parts.append("<span>%s</span>" % label)
    return '<nav class="breadcrumb" aria-label="Breadcrumb">' + '<span class="sep">/</span>'.join(parts) + "</nav>"


def category_icon(cat):
    return {
        "Property Intelligence": "layers",
        "Energy & Retrofit": "bolt",
        "Drone & Visual Inspection": "drone",
        "Roof & External": "roof",
    }[cat]


def cta_band(prefix, heading, text, primary=("Request an Assessment", "contact.html"), secondary=("Explore Services", "services.html")):
    return """
<section class="section section--tight">
  <div class="container">
    <div class="cta-band reveal">
      <div class="cta-band-text">
        <h2>{heading}</h2>
        <p>{text}</p>
      </div>
      <div class="cta-row">
        <a class="btn btn-primary" href="{prefix}{p_href}">{p_label}</a>
        <a class="btn btn-outline-light" href="{prefix}{s_href}">{s_label}</a>
      </div>
    </div>
  </div>
</section>
""".format(
        heading=heading, text=text, prefix=prefix,
        p_label=primary[0], p_href=primary[1], s_label=secondary[0], s_href=secondary[1],
    )


CARD_SIZES = "(max-width: 640px) 100vw, (max-width: 980px) 50vw, 380px"


def service_media(prefix, s, sizes=CARD_SIZES):
    if s.get("image"):
        return photo(prefix, s["image"], s["alt"], sizes=sizes)
    return ph("Photography to follow", s["icon"], "wide")


def service_card(prefix, s, show_category=False):
    cat_line = '<div class="eyebrow">%s</div>' % s["category"] if show_category else ""
    return """
<article class="card service-card reveal">
  <a class="card-media" href="{prefix}services/{slug}.html" tabindex="-1" aria-hidden="true">{media}<span class="card-media-icon">{icon}</span></a>
  <div class="card-body">
    {cat}
    <h3><a href="{prefix}services/{slug}.html">{name}</a></h3>
    <p>{summary}</p>
    <div class="card-foot">
      {badge}
      <span class="btn-ghost">Learn more {arrow}</span>
    </div>
  </div>
</article>
""".format(
        media=service_media(prefix, s), icon=icon(s["icon"], 18), cat=cat_line, name=s["short"], summary=s["summary"],
        badge=service_badges(s), prefix=prefix, slug=s["slug"],
        arrow=icon("arrow-right", 15, "icon"),
    )


def resource_card(prefix, r):
    return """
<a class="card resource-card reveal" href="{prefix}resources/{slug}.html">
  <div class="card-media">{photo}</div>
  <div class="card-body">
    <div class="resource-tag">{tag}</div>
    <h3>{title}</h3>
    <p>{summary}</p>
    <span class="btn-ghost">Read article {arrow}</span>
  </div>
</a>
""".format(
        prefix=prefix, slug=r["slug"], tag=r["tag"], title=r["title"], summary=r["summary"],
        photo=photo(prefix, r["image"], r["alt"], sizes=CARD_SIZES), arrow=icon("arrow-right", 15, "icon"),
    )


def credentials_strip(prefix):
    return """
<section class="cred-strip" aria-label="Qualifications and credentials">
  <div class="container cred-grid">
    <div class="cred-item cred-item--badge">
      {abbe}
      <div><strong>Domestic Energy Assessor</strong><span>ABBE-qualified</span></div>
    </div>
    <div class="cred-item">{i1}<div><strong>CAA-registered</strong><span>Flyer ID &amp; Operator ID</span></div></div>
    <div class="cred-item">{i2}<div><strong>Photographic evidence</strong><span>With every report</span></div></div>
    <div class="cred-item">{i3}<div><strong>Local &amp; independent</strong><span>{area}</span></div></div>
  </div>
</section>
""".format(abbe=ABBE_BADGE.format(prefix=prefix), i1=icon("shield-check", 22), i2=icon("camera", 22),
           i3=icon("map-pin", 22), area=SERVICE_AREA)


AUDIENCE = [
    ("Homeowners", "Understand your property, keep it well maintained, and get clear evidence of its condition."),
    ("Landlords", "EPCs, inspections and periodic records to help manage your properties with confidence."),
    ("Property managers & letting agents", "Structured inspection information, not just a folder of photographs."),
    ("Commercial property owners", "Building, roof and site documentation with professional visual evidence."),
    ("Property professionals", "A reliable source of visual evidence and property information for your clients."),
]


def audience_strip():
    items = "".join(
        '<div class="card reveal"><h4 style="margin-bottom:8px;">%s</h4><p style="font-size:0.88rem;margin:0;">%s</p></div>' % (name, desc)
        for name, desc in AUDIENCE
    )
    return """
<section class="section section--alt">
  <div class="container">
    <div class="section-head center">
      <span class="eyebrow">Who we work with</span>
      <h2>Built for everyone with a property to understand</h2>
      <p class="lede">From a single family home to a portfolio of let properties, the same clear approach applies.</p>
    </div>
    <div class="grid grid-3">%s</div>
  </div>
</section>
""" % items


# --------------------------------------------------------------------------
# HOMEPAGE
# --------------------------------------------------------------------------

def build_home():
    prefix = ""
    hero = """
<section class="hero">
  <div class="hero-bg">
    <img src="assets/img/hero-drone-house-1600.jpg"
         srcset="assets/img/hero-drone-house-900.jpg 900w, assets/img/hero-drone-house-1600.jpg 1600w, assets/img/hero-drone-house-2400.jpg 2400w"
         sizes="100vw" width="1600" height="905" alt="" fetchpriority="high">
  </div>
  <div class="container hero-inner">
    <span class="eyebrow eyebrow--light">EPCs &middot; Drone surveys &middot; Property inspection &middot; Worcestershire</span>
    <h1>Know your property.<br><span class="accent">Make better decisions.</span></h1>
    <p class="lede">Property inspection, energy assessment and aerial survey for homeowners, landlords and property professionals across {area}. We inspect, we measure, and we give you the evidence.</p>
    <div class="cta-row">
      <a class="btn btn-primary btn-lg" href="contact.html">Request an Assessment {arrow}</a>
      <a class="btn btn-outline-light btn-lg" href="services.html">Explore Our Services</a>
    </div>
  </div>
  <div class="hero-coords" aria-hidden="true"><span>52.19&deg; N</span><span>2.22&deg; W</span><span>Worcestershire</span></div>
</section>
""".format(area=SERVICE_AREA, arrow=icon("arrow-right", 16, "icon"))

    what_is = """
<section class="section">
  <div class="container two-col">
    <div>
      <span class="eyebrow">What is Property Intelligence?</span>
      <h2>Your property has a story. We help you understand it.</h2>
      <p class="lede">Most property owners have information scattered across EPCs, old photographs, contractor notes, maintenance records and inspection reports &mdash; if they have it at all. PCT Property Intelligence brings this together into a clearer, structured picture of your property, so you can see its condition, performance and history in one place.</p>
      <a class="btn-ghost" href="about.html">More about PCT {arrow}</a>
    </div>
    <div class="reveal">
      <div class="check-list card">
        <div class="check-item">{i1}<div><strong>EPCs &amp; energy records</strong><span>Brought into the same picture as everything else.</span></div></div>
        <div class="check-item">{i2}<div><strong>Photographs &amp; inspection findings</strong><span>Organised by property, not scattered across devices.</span></div></div>
        <div class="check-item">{i3}<div><strong>Maintenance &amp; contractor records</strong><span>A single reference point you can return to.</span></div></div>
        <div class="check-item">{i4}<div><strong>Roof, gutter &amp; external condition</strong><span>Documented clearly, with visual evidence.</span></div></div>
      </div>
    </div>
  </div>
</section>
""".format(
        arrow=icon("arrow-right", 15, "icon"),
        i1=icon("bolt", 19), i2=icon("camera", 19), i3=icon("clipboard", 19), i4=icon("roof", 19),
    )

    services_section = """
<section class="section section--alt">
  <div class="container">
    <div class="section-head center">
      <span class="eyebrow">Core Services</span>
      <h2>One consistent approach to understanding your property</h2>
      <p class="lede">Each service stands on its own, and combines with the others to build a fuller picture of your property.</p>
    </div>
    <div class="grid grid-3">
      {cards}
    </div>
  </div>
</section>
""".format(cards="".join(service_card(prefix, s) for s in SERVICES[:6]))

    technology = """
<section class="section">
  <div class="container two-col reverse">
    <div class="two-col-media reveal">
      <figure class="figure">
        {photo}
        <figcaption>{cam} Captured by PCT &mdash; drone survey of a semi-detached property</figcaption>
      </figure>
    </div>
    <div>
      <span class="eyebrow">Technology</span>
      <h2>Better information through better technology.</h2>
      <p class="lede">Technology is how PCT gathers more complete, more accurate information about your property &mdash; not a gimmick, and not the headline act.</p>
      <div class="check-list">
        <div class="check-item">{i1}<div><strong>Drone imagery</strong><span>Available now &mdash; aerial visual inspection of roofs and difficult-to-access areas.</span></div></div>
        <div class="check-item">{i2}<div><strong>High-resolution photography</strong><span>Available now &mdash; clear photographic evidence for every job.</span></div></div>
        <div class="check-item">{i3}<div><strong>Structured digital reporting</strong><span>Available now &mdash; findings and recommendations, clearly organised.</span></div></div>
        <div class="check-item">{i4}<div><strong>2D mapping &amp; 3D visualisation</strong><span>Planned &mdash; part of the wider property intelligence platform.</span></div></div>
      </div>
    </div>
  </div>
</section>
""".format(
        photo=photo(prefix, "aerial-house-real", "Aerial drone photograph of a semi-detached house with gravel driveway and rear garden"),
        cam=icon("camera", 14),
        i1=icon("drone", 19), i2=icon("camera", 19), i3=icon("chart", 19), i4=icon("grid", 19),
    )

    reporting = """
<section class="section section--navy" id="example-report">
  <div class="container">
    <div class="section-head center">
      <span class="eyebrow eyebrow--light">Reporting</span>
      <h2>See exactly what you receive.</h2>
      <p class="lede">Not just a report &mdash; a clear, structured record of your property's condition, with photographs, findings and recommendations you can actually use.</p>
    </div>
    <div class="report-mock reveal">
      <div class="report-mock-bar"><span class="dot"></span><span class="dot"></span><span class="dot"></span><span>Property Intelligence Report &mdash; Illustrative example</span></div>
      <div class="report-mock-body">
        <div>
          <div class="report-mock-title">Property Overview</div>
          <div class="report-row"><span>Property</span><span>14 Example Street</span></div>
          <div class="report-row"><span>Inspection date</span><span>September 2026</span></div>
          <div class="report-row"><span>Condition of roof tiles</span><span class="status-chip status-watch">1 cracked tile</span></div>
          <div class="report-row"><span>Roof observations</span><span class="status-chip status-watch">Moss build-up noted</span></div>
          <div class="report-row"><span>Gutter observations</span><span class="status-chip status-watch">Debris &amp; standing water</span></div>
          <div class="report-row"><span>Energy rating (EPC)</span><span class="epc-chip epc-d">D &middot; 61</span></div>
          <div class="report-note"><strong>Recommendation</strong><p>Gutter clearance recommended before autumn to prevent overflow. One cracked tile noted &mdash; refer to a roofer for replacement. Moss removal within 6&ndash;12 months.</p></div>
        </div>
        <div>
          <div class="report-mock-title">Photographs &amp; Evidence</div>
          <div class="report-photo-grid">
            {p1}{p2}{p3}{p4}{p5}{p6}
          </div>
        </div>
      </div>
    </div>
    <p class="report-footnote">Illustrative layout using real PCT inspection photographs &mdash; ask us for an example report for your property type.</p>
  </div>
</section>
""".format(**{"p%d" % (i + 1): '<figure class="report-thumb">%s<figcaption>%s</figcaption></figure>' % (
        photo(prefix, key, alt, sizes="160px"), label)
        for i, (key, label, alt) in enumerate([
            ("roof-moss-closeup", "Roof covering", "Moss growth across concrete roof tiles"),
            ("gutter-blocked", "Gutter run", "Standing water and moss in a gutter"),
            ("roof-broken-tile", "Tile defect", "Cracked roof tile beside a gutter"),
            ("gutter-debris", "Debris", "Moss debris collected in a gutter"),
            ("roof-gutter-edge", "Eaves line", "Moss along a gutter edge below the roof tiles"),
            ("aerial-house-real", "Aerial overview", "Aerial view of the property and plot"),
        ])})

    trust = """
<section class="section">
  <div class="container">
    <div class="section-head center">
      <span class="eyebrow">Trust &amp; Credentials</span>
      <h2>What we bring to every job</h2>
    </div>
    <div class="grid grid-4">
      <div class="card card--flat reveal">
        <div class="card-logo">{abbe}</div>
        <h3>ABBE-qualified Domestic Energy Assessor</h3>
        <p>Qualified to carry out Domestic Energy Assessments and produce Energy Performance Certificates.</p>
        <span class="badge badge-available"><span class="badge-dot"></span>Available now</span>
      </div>
      <div class="card card--flat reveal">
        <div class="card-icon">{i1}</div>
        <h3>CAA-registered drone operation</h3>
        <p>Operated under a valid Flyer ID and Operator ID, with a DJI Mini 5 and spare batteries for every job.</p>
        <span class="badge badge-available"><span class="badge-dot"></span>Available now</span>
      </div>
      <div class="card card--flat reveal">
        <div class="card-icon">{i2}</div>
        <h3>Retrofit Assessor</h3>
        <p>Qualification planned, extending PCT's assessment work into retrofit and energy improvement.</p>
        <span class="badge badge-soon"><span class="badge-dot"></span>Coming soon</span>
      </div>
      <div class="card card--flat reveal">
        <div class="card-icon">{i3}</div>
        <h3>Observation vs. recommendation</h3>
        <p>Every report separates what was actually observed from what may be worth investigating further.</p>
        <span class="badge badge-available"><span class="badge-dot"></span>Every report</span>
      </div>
    </div>
  </div>
</section>
""".format(abbe=ABBE_BADGE.format(prefix=prefix).replace("<img ", '<img loading="lazy" '),
           i1=icon("shield-check", 22), i2=icon("leaf", 22), i3=icon("clipboard", 22))

    local_band = """
<section class="split-band">
  <div class="split-band-media">{photo}</div>
  <div class="split-band-body">
    <span class="eyebrow eyebrow--light">Local &amp; independent</span>
    <h2>A real, local business &mdash; not a call centre.</h2>
    <p>PCT Property Intelligence is based in Worcestershire and works across the surrounding area. You deal directly with PCT from first enquiry to final report &mdash; no call centres, no middlemen.</p>
    <div class="check-list check-list--light">
      <div class="check-item">{c}<span>Direct contact from enquiry to report</span></div>
      <div class="check-item">{c}<span>Clear pricing agreed before any work</span></div>
      <div class="check-item">{c}<span>Reports written in plain English</span></div>
    </div>
    <a class="btn btn-primary" href="about.html">About PCT {arrow}</a>
  </div>
</section>
""".format(photo=photo(prefix, "car-cottage", "PCT Property Intelligence branded black car parked outside a Cotswold stone cottage",
                       sizes="(max-width: 980px) 100vw, 50vw"),
           c=icon("check", 18), arrow=icon("arrow-right", 15, "icon"))

    portal_teaser = """
<section class="section">
  <div class="container two-col">
    <div>
      <span class="eyebrow">The Bigger Picture</span>
      <h2>Building toward a full property intelligence platform</h2>
      <p class="lede">PCT Property Intelligence is more than a single inspection. Over time, every customer will be able to book an inspection, receive a report, and access an ongoing digital record of their property through a secure Client Portal.</p>
      <div class="check-list">
        <div class="check-item">{c}<span>Book an assessment and receive photographs, findings and a report</span></div>
        <div class="check-item">{c}<span>Access everything through a secure customer portal</span></div>
        <div class="check-item">{c}<span>Build an ongoing digital record of your property over time</span></div>
      </div>
      <a class="btn btn-secondary" style="margin-top:24px;" href="portal.html">About the Client Portal {arrow}</a>
    </div>
    <div class="reveal">
      <div class="portal-panel">
        <div class="portal-side">
          <div class="brand-mini"><span class="dotmark"></span>My Property Intelligence</div>
          <div class="portal-nav-item active">{p1} My Properties</div>
          <div class="portal-nav-item">{p2} Reports</div>
          <div class="portal-nav-item">{p3} Inspection History</div>
          <div class="portal-nav-item">{p4} Documents</div>
        </div>
        <div class="portal-main">
          <div class="portal-property-card"><div><div class="addr">14 Example Street</div><div class="meta">Last inspection: Sept 2026</div></div><span class="badge badge-neutral">Illustrative</span></div>
          <div class="portal-property-card"><div><div class="addr">2 Sample Cottages</div><div class="meta">Report ready to view</div></div><span class="badge badge-neutral">Illustrative</span></div>
        </div>
      </div>
    </div>
  </div>
</section>
""".format(c=icon("check", 18), arrow=icon("arrow-right", 15, "icon"),
           p1=icon("home", 15), p2=icon("document", 15), p3=icon("history", 15), p4=icon("layers", 15))

    resources_section = """
<section class="section section--alt">
  <div class="container">
    <div class="section-head center">
      <span class="eyebrow">Resources</span>
      <h2>Property knowledge, explained clearly</h2>
    </div>
    <div class="grid grid-3">
      {cards}
    </div>
    <div style="text-align:center;margin-top:36px;">
      <a class="btn btn-secondary" href="resources.html">Browse all resources</a>
    </div>
  </div>
</section>
""".format(cards="".join(resource_card(prefix, r) for r in RESOURCES))

    final_cta = cta_band(
        prefix,
        "Ready to understand your property better?",
        "Tell us what you need, and we'll recommend the right combination of services.",
    )

    content = (hero + credentials_strip(prefix) + what_is + services_section + technology + reporting
               + trust + local_band + audience_strip() + portal_teaser + resources_section + final_cta)

    write("index.html", page(
        "index",
        "Property Assessment, Inspection & Intelligence",
        "EPCs from an ABBE-qualified Domestic Energy Assessor, CAA-registered drone roof inspections, and gutter inspections with clear photo reports across Worcestershire.",
        content, prefix=prefix, active="home", schema=LOCAL_BUSINESS_SCHEMA,
        seo_title="EPCs, Drone Roof & Property Inspections in Worcestershire",
        head_extra=('<link rel="preload" as="image" href="assets/img/hero-drone-house-1600.jpg" '
                    'imagesrcset="assets/img/hero-drone-house-900.jpg 900w, assets/img/hero-drone-house-1600.jpg 1600w, '
                    'assets/img/hero-drone-house-2400.jpg 2400w" imagesizes="100vw" fetchpriority="high">'),
    ))


# --------------------------------------------------------------------------
# ABOUT
# --------------------------------------------------------------------------

def build_about():
    prefix = ""
    hero = """
<section class="page-hero">
  <div class="container">
    {crumb}
    <span class="eyebrow">About PCT</span>
    <h1>A modern, independent property intelligence business.</h1>
    <p class="lede">PCT Property Intelligence was built around a simple idea: property owners deserve clear, well-documented information about the properties they own, manage or let &mdash; not just a verbal opinion and a handful of photographs.</p>
  </div>
</section>
""".format(crumb=breadcrumb(prefix, [("Home", "index.html"), ("About PCT", None)])) + credentials_strip(prefix)

    story = """
<section class="section">
  <div class="container two-col">
    <div class="reveal">{photo}</div>
    <div>
      <span class="eyebrow">Our Story</span>
      <h2>Practical property knowledge, combined with modern technology.</h2>
      <p>PCT Property Intelligence is a new UK property-services and property-intelligence business, built around professional property assessment, inspection, energy information and detailed visual reporting.</p>
      <p>The business is being developed deliberately and transparently: services are added as the right equipment, qualifications and processes are in place, rather than promised before they exist. What's available today is genuinely available. What's coming is clearly marked as coming soon.</p>
      <p>The result is a company built on practical property knowledge, careful documentation and modern inspection technology &mdash; used to give customers better information about the property in front of them, not to impress with gadgets.</p>
    </div>
  </div>
</section>
""".format(photo=photo(prefix, "car-cottage", "PCT Property Intelligence branded car outside a Cotswold stone cottage", cls="photo--rounded"))

    principles = """
<section class="section section--alt">
  <div class="container">
    <div class="section-head center">
      <span class="eyebrow">What We Believe</span>
      <h2>The principles behind PCT Property Intelligence</h2>
    </div>
    <div class="grid grid-4">
      <div class="card reveal"><div class="card-icon">{i1}</div><h3>Show, don't just tell</h3><p>Photographic and visual evidence, not just a verbal summary of what was found.</p></div>
      <div class="card reveal"><div class="card-icon">{i2}</div><h3>Clear, structured reporting</h3><p>Observations and recommendations are always kept separate and clearly labelled.</p></div>
      <div class="card reveal"><div class="card-icon">{i3}</div><h3>Honest about capability</h3><p>We only advertise services, equipment and qualifications we actually have.</p></div>
      <div class="card reveal"><div class="card-icon">{i4}</div><h3>Property first, technology second</h3><p>Drones, mapping and digital reporting exist to serve better information &mdash; not the other way around.</p></div>
    </div>
  </div>
</section>
""".format(i1=icon("camera", 22), i2=icon("clipboard", 22), i3=icon("shield-check", 22), i4=icon("compass", 22))

    vision = """
<section class="section">
  <div class="container two-col reverse">
    <div class="two-col-media reveal">
      <div class="timeline card">
        <div class="timeline-item"><time>Today</time><h4>Inspection, documentation &amp; EPCs</h4><p>Drone inspection, roof &amp; gutter inspection, photography, visual property records, and EPCs from an ABBE-qualified Domestic Energy Assessor.</p></div>
        <div class="timeline-item"><time>Next</time><h4>Retrofit assessment</h4><p>Retrofit Assessor qualification, building on the energy assessment work already in place.</p></div>
        <div class="timeline-item"><time>Future</time><h4>Digital property intelligence platform</h4><p>A secure client portal holding every report, photo and record for your property.</p></div>
      </div>
    </div>
    <div>
      <span class="eyebrow">Where We're Heading</span>
      <h2>Building toward a broader property intelligence platform</h2>
      <p class="lede">PCT Property Intelligence is designed from day one to grow into more than a single inspection visit &mdash; eventually combining assessment, energy information, drone imagery, mapping and reporting into one ongoing digital property record.</p>
      <a class="btn btn-secondary" href="portal.html">About the Client Portal {arrow}</a>
    </div>
  </div>
</section>
""".format(arrow=icon("arrow-right", 15, "icon"))

    equipment = """
<section class="section section--alt">
  <div class="container">
    <div class="section-head center">
      <span class="eyebrow">Equipment &amp; Technology</span>
      <h2>Modern inspection technology, used with purpose</h2>
      <p class="lede">Technology is incorporated where it genuinely improves the information you receive.</p>
    </div>
    <div class="grid grid-4">
      <div class="card reveal"><div class="card-logo">{abbe}</div><h3>Energy assessment</h3><p>ABBE-qualified Domestic Energy Assessor, producing EPCs and energy information to a recognised standard.</p></div>
      <div class="card reveal"><div class="card-icon">{i1}</div><h3>Aerial inspection</h3><p>DJI Mini 5 with additional flight batteries, operated under a registered Flyer ID and Operator ID, for safe, controlled aerial inspection.</p></div>
      <div class="card reveal"><div class="card-icon">{i2}</div><h3>Gutter inspection</h3><p>Gutters and downpipes checked from the ground and the air, with photographs of every blockage found. Gutter cleaning is coming soon.</p></div>
      <div class="card reveal"><div class="card-icon">{i3}</div><h3>Reporting &amp; documentation</h3><p>Professional computing and office infrastructure used to produce clear, well-organised reports for every job.</p></div>
    </div>
  </div>
</section>
""".format(i1=icon("drone", 22), i2=icon("droplet", 22), i3=icon("document", 22),
           abbe=ABBE_BADGE.format(prefix=prefix).replace("<img ", '<img loading="lazy" '))

    content = hero + story + principles + vision + equipment + cta_band(
        prefix, "Want to know more before you book?", "Get in touch and we'll talk you through exactly what's involved.",
        primary=("Contact Us", "contact.html"), secondary=("View Services", "services.html"),
    )

    write("about.html", page(
        "about", "About PCT Property Intelligence",
        "PCT Property Intelligence is an independent Worcestershire property inspection business: ABBE-qualified EPCs, CAA-registered drone surveys and clear reports.",
        content, prefix=prefix, active="about",
        seo_title="About PCT – Independent Property Inspection, Worcestershire",
    ))


# --------------------------------------------------------------------------
# SERVICES OVERVIEW
# --------------------------------------------------------------------------

def build_services_overview():
    prefix = ""
    hero = """
<section class="page-hero">
  <div class="container">
    {crumb}
    <span class="eyebrow">Services</span>
    <h1>Property assessment, inspection and documentation services</h1>
    <p class="lede">Every service fits under one idea: property intelligence. Use one on its own, or combine several for a fuller picture of your property.</p>
  </div>
</section>
""".format(crumb=breadcrumb(prefix, [("Home", "index.html"), ("Services", None)]))

    cats = {}
    for s in SERVICES:
        cats.setdefault(s["category"], []).append(s)

    groups = ""
    for cat in CATEGORY_ORDER:
        groups += """
<section class="section {alt}">
  <div class="container">
    <div class="category-strip"><span class="category-chip">{cicon} {cat}</span></div>
    <div class="grid grid-3">{cards}</div>
  </div>
</section>
""".format(
            alt="section--alt" if CATEGORY_ORDER.index(cat) % 2 else "",
            cicon=icon(category_icon(cat), 16), cat=cat,
            cards="".join(service_card(prefix, s) for s in cats[cat]),
        )

    combine = """
<section class="section">
  <div class="container">
    <div class="section-head center">
      <span class="eyebrow">Combine Services</span>
      <h2>Most jobs work best combined</h2>
      <p class="lede">For example, a Roof Inspection often pairs naturally with a Drone Inspection and a Gutter Inspection &mdash; giving you a fuller picture in a single visit.</p>
    </div>
    <div class="pill-list" style="justify-content:center;">
      <span class="pill">Roof Inspection + Drone Inspection</span>
      <span class="pill">Gutter Inspection + Roof Inspection</span>
      <span class="pill">Property Documentation + Photography</span>
      <span class="pill">Drone Inspection + Property Documentation</span>
    </div>
  </div>
</section>
"""

    content = hero + groups + combine + cta_band(prefix, "Not sure which service you need?", "Tell us a little about your property and we'll recommend the right combination.")

    write("services.html", page(
        "services", "Property Services",
        "EPCs, drone roof inspections, roof and gutter inspections, property records and aerial photography across Worcestershire. Book one service or combine several.",
        content, prefix=prefix, active="services",
        seo_title="EPC, Drone & Property Inspection Services in Worcestershire",
    ))


# --------------------------------------------------------------------------
# SERVICE DETAIL CONTENT
# --------------------------------------------------------------------------

SERVICE_DETAIL = {
    "energy-assessment-epc": {
        "intro": "A Domestic Energy Assessment produces the Energy Performance Certificate (EPC) that tells you, your buyer or your tenant how efficiently a property uses energy. PCT's assessments are carried out by an ABBE-qualified Domestic Energy Assessor, and the energy information sits alongside every other piece of property information in one place.",
        "involves": [
            ("clipboard", "A full internal and external survey", "Measuring and recording construction, insulation, heating, hot water, glazing and lighting."),
            ("bolt", "A standard energy calculation", "Producing the EPC energy efficiency rating (A&ndash;G) using the approved methodology."),
            ("document", "A lodged, valid certificate", "Registered on the official government EPC register."),
        ],
        "receive": [
            ("chart", "Your property's EPC rating", "A clear A&ndash;G energy efficiency rating."),
            ("leaf", "Improvement suggestions", "Practical recommendations to improve efficiency."),
            ("document", "A lodged certificate", "Valid for the standard 10-year period."),
        ],
        "faq": [
            ("Is this service available now?", "Yes. Domestic Energy Assessments are carried out by an ABBE-qualified Domestic Energy Assessor. Get in touch with your property details and we'll confirm availability and price."),
            ("How long does an assessment take?", "Most homes take around an hour on site, depending on size and access. You'll need to give access to every room, the loft if there is one, and the boiler and hot water cylinder."),
            ("Do I legally need an EPC?", "Most UK properties need a valid EPC when built, sold or let. If you're unsure whether yours is still valid, get in touch and we can point you in the right direction."),
            ("Will energy information link to my other property records?", "Yes &mdash; that's the point. Energy information is designed to sit inside the same property record as your inspection and maintenance history."),
        ],
    },
    "retrofit-assessment": {
        "intro": "A Retrofit Assessment looks at how a property could be improved to perform better &mdash; more comfortable, more efficient, and better prepared for future energy standards. It's assessment and information first, giving you a clear starting point before any improvement work is planned.",
        "involves": [
            ("clipboard", "Property condition review", "Understanding the building's construction and current performance."),
            ("bolt", "Energy performance context", "Assessed alongside EPC and energy information where available."),
            ("document", "Retrofit information report", "A clear summary to support future improvement decisions."),
        ],
        "receive": [
            ("document", "A retrofit information report", "Practical, property-specific findings."),
            ("leaf", "A starting point for improvements", "Information to support planning future energy upgrades."),
            ("layers", "Integration with your property record", "Kept alongside your inspection and energy history."),
        ],
        "faq": [
            ("Is this service available now?", "Not yet. The Retrofit Assessor qualification is planned next, building on PCT's existing Domestic Energy Assessor qualification."),
            ("Does a Retrofit Assessment include the improvement work itself?", "No &mdash; this is an assessment and information service. It gives you a clear picture to help plan any future improvement work, carried out by appropriately qualified installers."),
            ("How does this relate to the EPC?", "Retrofit assessment builds on the same property and energy information used for an EPC, so the two naturally sit together in your property record."),
        ],
    },
    "drone-inspection": {
        "intro": "Some parts of a property are difficult, slow or risky to inspect from the ground or with access equipment. Drone inspection gives you a safe, efficient way to access difficult-to-see areas &mdash; roofs, chimneys, tall elevations and large sites &mdash; without unnecessary scaffolding or ladders.",
        "involves": [
            ("shield-check", "CAA-registered flight", "Operated under a valid Flyer ID and Operator ID, with appropriate flight planning."),
            ("drone", "Aerial visual inspection", "High-resolution imagery of roofs, gutters, chimneys and elevations."),
            ("camera", "Photographic documentation", "Clear images organised by property and inspection date."),
        ],
        "receive": [
            ("camera", "Aerial photographs", "Clear, high-resolution images of hard-to-reach areas."),
            ("document", "Visual inspection notes", "Condition observations based on what was seen."),
            ("shield-check", "Peace of mind", "No need for scaffolding or access equipment for a visual check."),
        ],
        "faq": [
            ("Is drone inspection available now?", "Yes &mdash; drone inspection is available now, operated under a registered Flyer ID and Operator ID."),
            ("Does drone inspection replace a structural survey?", "No. Drone inspection provides visual evidence and condition observations &mdash; it does not replace a structural survey or other regulated specialist assessment."),
            ("What areas can be inspected?", "Roofs, gutters, chimneys, tall or large building elevations, and other areas that are difficult or unsafe to access from the ground."),
            ("Is it weather dependent?", "Yes. Flights are only carried out when conditions are safe and suitable, in line with CAA regulations."),
        ],
    },
    "roof-inspection": {
        "intro": "A Roof Inspection gives you a clear picture of your roof's visible condition, combining ground-level observation with aerial inspection where useful. You receive photographic evidence and plain-language observations &mdash; not just a verbal opinion.",
        "involves": [
            ("roof", "Ground-level visual inspection", "A thorough external assessment from accessible vantage points."),
            ("drone", "Aerial inspection where useful", "Combined with drone inspection for a fuller picture."),
            ("camera", "Photographic evidence", "Clear images of anything noted during the inspection."),
        ],
        "receive": [
            ("document", "A written inspection summary", "Plain-language observations, organised by roof area."),
            ("camera", "Supporting photographs", "Visual evidence for everything noted."),
            ("clipboard", "Recommendations where relevant", "Clearly separated from what was actually observed."),
        ],
        "faq": [
            ("Is this a structural survey?", "No. This is a visual inspection providing condition observations and photographic evidence &mdash; not a structural engineering or roofing specialist opinion."),
            ("Will you get on my roof?", "Inspections are carried out using ground-level and aerial techniques appropriate to the property, avoiding unnecessary access risk."),
            ("Can this be combined with other services?", "Yes &mdash; Roof Inspection is often combined with Drone Inspection and Gutter Inspection in a single visit."),
        ],
    },
    "gutter-inspection-cleaning": {
        "intro": "Gutters can become heavily blocked with moss and debris without it ever being obvious from ground level. Our gutter inspection identifies blockages, moss, debris and overflow risks, with photographic evidence so you're shown the condition, not just told. Gutter cleaning is coming soon.",
        "involves": [
            ("droplet", "Blockage &amp; debris inspection", "Identifying moss, debris, overflow risk and visible defects."),
            ("wrench", "Downpipe &amp; overflow check", "Looking for visible issues affecting water flow."),
            ("camera", "Photographic evidence", "Clear images of every blockage, defect or overflow risk found, from the ground or the air."),
        ],
        "receive": [
            ("camera", "Before photographs", "Clear evidence of the starting condition."),
            ("droplet", "Inspection findings", "What was found, in plain language."),
            ("clipboard", "Clear recommendations", "What needs clearing or repairing, and how urgent it is."),
        ],
        "faq": [
            ("Is gutter cleaning available now?", "Not yet. Gutter inspection is available now; gutter cleaning is coming soon. In the meantime, our inspection shows exactly where your gutters need clearing, so you or your contractor know what to tackle."),
            ("How often should gutters be cleaned?", "It depends on nearby trees and the property type. Read our guide: <a href=\"resources/how-often-should-gutters-be-cleaned.html\">How often should gutters be cleaned?</a>"),
            ("Will I actually see evidence my gutters are clear?", "Yes &mdash; that's central to how we work. You receive before and after photographs, not just a verbal confirmation."),
        ],
    },
    "property-documentation": {
        "intro": "Property Documentation creates a structured, professional record of your property's condition &mdash; useful for landlords, property managers, buyers, sellers and homeowners who simply want a clear reference point. It's organised information, not just a folder of photographs.",
        "involves": [
            ("clipboard", "A structured property walkthrough", "Covering the areas relevant to your needs."),
            ("camera", "Photographic documentation", "Clear, organised images of the property's condition."),
            ("document", "A written summary", "Findings presented in a clear, structured format."),
        ],
        "receive": [
            ("document", "A structured property record", "Organised information, not a random set of photos."),
            ("camera", "Photographic evidence", "A clear visual record of condition at the time of the visit."),
            ("layers", "A record you can keep on file", "Useful for property files, insurance or future reference."),
        ],
        "faq": [
            ("Who is this useful for?", "Landlords documenting property condition, property managers keeping structured records, and homeowners who simply want a clear reference point for their property."),
            ("Can this be combined with an inspection?", "Yes &mdash; Property Documentation pairs naturally with Roof Inspection, Gutter Inspection or Drone Inspection."),
            ("Do I receive digital or printed copies?", "Reports and photographs are provided digitally, ready to be kept on file or shared as needed."),
        ],
    },
    "photography-visual-records": {
        "intro": "Sometimes what you need is simply clear, professional photography &mdash; of a property, a specific area, or before and after a piece of work. This service provides high-quality visual records you can rely on.",
        "involves": [
            ("camera", "Professional photography", "High-resolution images suited to the property and purpose."),
            ("drone", "Aerial photography where useful", "Combined with drone imagery for wider or elevated views."),
            ("layers", "Organised delivery", "Images organised by property, date and purpose."),
        ],
        "receive": [
            ("camera", "High-resolution photographs", "Clear, professional images of your property."),
            ("history", "Before &amp; after documentation", "Useful evidence around any work carried out."),
            ("document", "Organised image sets", "Delivered in a clear, usable format."),
        ],
        "faq": [
            ("What is this useful for?", "Marketing a property, documenting condition before or after works, insurance purposes, or simply keeping a clear visual record."),
            ("Can you photograph hard-to-reach areas?", "Yes &mdash; this service can be combined with Drone Inspection for aerial and elevated photography."),
            ("How are photographs delivered?", "Digitally, organised by property and date, ready to keep or share."),
        ],
    },
}


def build_service_pages():
    for s in SERVICES:
        prefix = "../"
        d = SERVICE_DETAIL[s["slug"]]
        related = [x for x in SERVICES if x["category"] == s["category"] and x["slug"] != s["slug"]]
        if len(related) < 2:
            related += [x for x in SERVICES if x not in related and x["slug"] != s["slug"]][: 2 - len(related)]

        hero = """
<section class="page-hero{mod}">
  {bg}
  <div class="container">
    {crumb}
    <div class="page-hero-flex">
      <div>
        <span class="eyebrow eyebrow--light">{cat}</span>
        <h1>{name}</h1>
        <p class="lede">{intro}</p>
      </div>
      {badge}
    </div>
  </div>
</section>
""".format(
            mod=" page-hero--image" if s.get("image") else "",
            bg=('<div class="page-hero-bg">%s</div>' % photo(prefix, s["image"], "", sizes="100vw", eager=True)) if s.get("image") else "",
            crumb=breadcrumb(prefix, [("Home", "index.html"), ("Services", "services.html"), (s["short"], None)]),
            cat=s["category"], name=s["name"], intro=d["intro"],
            badge='<div class="page-hero-badge">' + service_badges(s) + "</div>",
        )

        involves = """
<section class="section">
  <div class="container two-col">
    <div class="reveal">{media}</div>
    <div>
      <span class="eyebrow">What's Involved</span>
      <h2>How this service works</h2>
      <div class="check-list" style="margin-top:24px;">{items}</div>
    </div>
  </div>
</section>
""".format(
            media=(photo(prefix, s["detail"][0], s["detail"][1], cls="photo--rounded") if s.get("image")
                   else ph(s["name"] + " &mdash; photography to follow", s["icon"], "square")),
            items="".join(
                '<div class="check-item">%s<div><strong>%s</strong><span>%s</span></div></div>' % (icon(i, 19), t, desc)
                for i, t, desc in d["involves"]
            ),
        )

        receive = """
<section class="section section--alt">
  <div class="container">
    <div class="section-head center">
      <span class="eyebrow">What You Receive</span>
      <h2>Clear, usable outputs</h2>
    </div>
    <div class="grid grid-3">
      {cards}
    </div>
  </div>
</section>
""".format(
            cards="".join(
                '<div class="card reveal"><div class="card-icon">%s</div><h3>%s</h3><p>%s</p></div>' % (icon(i, 22), t, desc)
                for i, t, desc in d["receive"]
            )
        )

        faq = """
<section class="section">
  <div class="container" style="max-width:820px;">
    <div class="section-head">
      <span class="eyebrow">Frequently Asked</span>
      <h2>Questions about {short}</h2>
    </div>
    <div>{items}</div>
  </div>
</section>
""".format(
            short=s["short"],
            items="".join(
                """
<div class="accordion-item">
  <button class="accordion-trigger" aria-expanded="false">{q}{plus}</button>
  <div class="accordion-panel"><div class="accordion-panel-inner"><p>{a}</p></div></div>
</div>
""".format(q=q, a=a, plus='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M12 5v14M5 12h14"/></svg>')
                for q, a in d["faq"]
            ),
        )

        related_html = """
<section class="section section--alt">
  <div class="container">
    <div class="section-head center">
      <span class="eyebrow">Related Services</span>
      <h2>Often combined with {short}</h2>
    </div>
    <div class="grid grid-3">{cards}</div>
  </div>
</section>
""".format(short=s["short"], cards="".join(service_card(prefix, r, show_category=True) for r in related[:3]))

        content = hero + involves + receive + faq + related_html + cta_band(
            prefix, "Interested in " + s["short"] + "?",
            "Request an assessment and tell us about your property &mdash; we'll confirm exactly what's involved.",
        )

        url = "%s/services/%s.html" % (DOMAIN, s["slug"])
        service = {
            "@type": "Service",
            "@id": url + "#service",
            "name": s["name"],
            "serviceType": s["name"],
            "url": url,
            "provider": {"@id": BUSINESS_ID, "@type": "ProfessionalService", "name": "PCT Property Intelligence", "url": DOMAIN + "/"},
            "areaServed": AREA_SERVED,
            "description": s["meta"],
        }
        if s.get("image"):
            service["image"] = "%s/assets/img/%s-1600.jpg" % (DOMAIN, s["image"])
        schema = schema_tag({
            "@context": "https://schema.org",
            "@graph": [
                service,
                breadcrumb_schema([("Home", ""), ("Services", "services.html"), (s["short"], "services/%s.html" % s["slug"])]),
                {
                    "@type": "FAQPage",
                    "mainEntity": [
                        {"@type": "Question", "name": strip_tags(q),
                         "acceptedAnswer": {"@type": "Answer", "text": strip_tags(a)}}
                        for q, a in d["faq"]
                    ],
                },
            ],
        })

        write("services/%s.html" % s["slug"], page(
            "services/" + s["slug"], s["name"],
            s["meta"], content, prefix=prefix, active="services", schema=schema,
            seo_title=s["seo_title"], og_image=s.get("image") or "hero-drone-house",
        ))


# --------------------------------------------------------------------------
# CONTACT / QUOTE FORM
# --------------------------------------------------------------------------

def build_contact():
    prefix = ""
    hero = """
<section class="page-hero">
  <div class="container">
    {crumb}
    <span class="eyebrow">Contact</span>
    <h1>Request an assessment</h1>
    <p class="lede">Tell us about your property and what you need, and we'll come back to you with clear next steps &mdash; usually within one working day.</p>
  </div>
</section>
""".format(crumb=breadcrumb(prefix, [("Home", "index.html"), ("Contact", None)]))

    service_checks = "".join(
        '<label class="service-check"><input type="checkbox" name="additional-services" value="%s"> %s</label>'
        % (s["short"], s["short"])
        for s in SERVICES
    )

    form = """
<section class="section">
  <div class="container two-col" style="align-items:flex-start;">
    <div>
      <div class="form-card reveal">
        <h2 style="margin-bottom:6px;">Tell us about your property</h2>
        <p class="text-muted" style="margin-bottom:24px;font-size:0.9rem;">Fields marked * are required. We'll never share your details &mdash; see our <a href="privacy-policy.html" style="text-decoration:underline;">Privacy Policy</a>.</p>
        <form data-quote-form name="property-assessment-enquiry" data-netlify="true" netlify-honeypot="bot-field">
          <input type="hidden" name="form-name" value="property-assessment-enquiry">
          <p class="visually-hidden"><label>Don't fill this in: <input name="bot-field"></label></p>

          <div class="form-grid">
            <div class="form-field"><label for="name">Full name *</label><input id="name" name="name" type="text" required autocomplete="name"></div>
            <div class="form-field"><label for="email">Email *</label><input id="email" name="email" type="email" required autocomplete="email"></div>
            <div class="form-field"><label for="telephone">Telephone</label><input id="telephone" name="telephone" type="tel" autocomplete="tel"></div>
            <div class="form-field"><label for="contact-method">Preferred contact method</label>
              <select id="contact-method" name="preferred-contact-method">
                <option value="Email">Email</option>
                <option value="Phone">Phone</option>
                <option value="Either">Either</option>
              </select>
            </div>
            <div class="form-field full"><label for="address">Property address *</label><input id="address" name="property-address" type="text" required autocomplete="street-address"></div>
            <div class="form-field"><label for="postcode">Postcode *</label><input id="postcode" name="postcode" type="text" required autocomplete="postal-code"></div>
            <div class="form-field"><label for="property-type">Property type</label>
              <select id="property-type" name="property-type">
                <option value="">Select&hellip;</option>
                <option>Detached house</option>
                <option>Semi-detached house</option>
                <option>Terraced house</option>
                <option>Bungalow</option>
                <option>Flat / apartment</option>
                <option>Commercial property</option>
                <option>Other</option>
              </select>
            </div>
          </div>

          <div class="form-field full">
            <label for="primary-service">Primary service required *</label>
            <select id="primary-service" name="primary-service" required>
              <option value="">Select a service&hellip;</option>
              {service_options}
            </select>
          </div>

          <div class="form-field full">
            <label>Additional services (optional)</label>
            <span class="hint" style="margin-bottom:8px;display:block;">Select any others you'd like included in the same visit.</span>
            <div class="service-check-grid">{service_checks}</div>
          </div>

          <div class="form-grid">
            <div class="form-field"><label for="preferred-date">Preferred date</label><input id="preferred-date" name="preferred-date" type="date"></div>
            <div class="form-field"><label for="property-size">Approximate property size</label><input id="property-size" name="property-size" type="text" placeholder="e.g. 3-bed semi"></div>
          </div>

          <div class="form-field full">
            <label for="description">Description of requirements</label>
            <textarea id="description" name="description" placeholder="Tell us anything that will help &mdash; access notes, specific concerns, or areas you'd like inspected."></textarea>
          </div>

          <div class="form-field full">
            <label>Photographs (optional)</label>
            <div class="file-drop">{upload_icon}Photo upload is coming soon on the live site &mdash; for now, feel free to attach photographs when you reply to our confirmation email.</div>
          </div>

          <div class="checkbox-row" style="margin-top:6px;">
            <input type="checkbox" id="consent" name="consent" required>
            <label for="consent">I consent to PCT Property Intelligence storing and using my details to respond to this enquiry, in line with the <a href="privacy-policy.html" style="text-decoration:underline;">Privacy Policy</a>. *</label>
          </div>

          <button class="btn btn-primary btn-block" type="submit" style="margin-top:22px;">Send Request {arrow}</button>
          <div class="form-status" data-form-status></div>
        </form>
      </div>
    </div>
    <div class="reveal">
      <div class="card" style="margin-bottom:20px;">
        <div class="card-icon">{i_mail}</div>
        <h3>Email</h3>
        <p><a href="mailto:{email}" style="text-decoration:underline;">{email}</a></p>
      </div>
      <div class="card" style="margin-bottom:20px;">
        <div class="card-icon">{i_pin}</div>
        <h3>Coverage area</h3>
        <p>{area}. Get in touch if you're just outside this area &mdash; we may still be able to help.</p>
      </div>
      <div class="card">
        <div class="card-icon">{i_clock}</div>
        <h3>Response time</h3>
        <p>We aim to reply to every enquiry within one working day.</p>
      </div>
    </div>
  </div>
</section>
""".format(
        service_options="".join('<option value="%s">%s</option>' % (s["short"], s["short"]) for s in SERVICES),
        service_checks=service_checks,
        arrow=icon("arrow-right", 16, "icon"),
        upload_icon=icon("upload", 22),
        i_mail=icon("mail", 22), i_pin=icon("map-pin", 22), i_clock=icon("calendar", 22),
        email=BUSINESS_EMAIL, area=SERVICE_AREA,
    )

    content = hero + form

    write("contact.html", page(
        "contact", "Contact & Request an Assessment",
        "Request an EPC, drone roof inspection or property inspection in Worcestershire. Tell us about your property and we'll reply within one working day.",
        content, prefix=prefix, active="contact",
        seo_title="Request an EPC or Property Inspection Quote",
    ))


# --------------------------------------------------------------------------
# CLIENT PORTAL (concept / coming soon)
# --------------------------------------------------------------------------

def build_portal():
    prefix = ""
    hero = """
<section class="page-hero">
  <div class="container">
    {crumb}
    <div class="page-hero-flex">
      <div>
        <span class="eyebrow">Client Portal</span>
        <h1>Your property record, in one secure place</h1>
        <p class="lede">The Client Portal is the long-term home for your reports, photographs, inspection history and property information. Account access is planned for a later phase &mdash; here's what it will include.</p>
      </div>
      <div>{badge}</div>
    </div>
  </div>
</section>
""".format(crumb=breadcrumb(prefix, [("Home", "index.html"), ("Client Portal", None)]), badge=status_badge("soon"))

    preview = """
<section class="section">
  <div class="container two-col">
    <div class="reveal">
      <div class="portal-panel">
        <div class="portal-side">
          <div class="brand-mini"><span class="dotmark"></span>My Property Intelligence</div>
          <div class="portal-nav-item active">{p1} My Properties</div>
          <div class="portal-nav-item">{p2} Reports</div>
          <div class="portal-nav-item">{p3} Inspection History</div>
          <div class="portal-nav-item">{p4} Photos &amp; Drone Imagery</div>
          <div class="portal-nav-item">{p5} Documents</div>
        </div>
        <div class="portal-main">
          <div class="portal-property-card"><div><div class="addr">14 Example Street</div><div class="meta">Energy rating: Coming soon &middot; Last inspection: Sept 2026</div></div><span class="badge badge-neutral">Illustrative</span></div>
          <div class="portal-property-card"><div><div class="addr">2 Sample Cottages</div><div class="meta">Report ready to view</div></div><span class="badge badge-neutral">Illustrative</span></div>
          <div class="portal-property-card"><div><div class="addr">Unit 4, Sample Business Park</div><div class="meta">Roof inspection scheduled</div></div><span class="badge badge-neutral">Illustrative</span></div>
        </div>
      </div>
    </div>
    <div>
      <span class="eyebrow">What's Coming</span>
      <h2>Each property gets its own digital profile</h2>
      <div class="check-list">
        <div class="check-item">{c}<div><strong>Reports &amp; findings</strong><span>Every report, downloadable and searchable in one place.</span></div></div>
        <div class="check-item">{c}<div><strong>Inspection history</strong><span>A timeline of every visit and what was found.</span></div></div>
        <div class="check-item">{c}<div><strong>Photographs &amp; drone imagery</strong><span>Organised by property, date and inspection.</span></div></div>
        <div class="check-item">{c}<div><strong>2D mapping &amp; 3D imagery</strong><span>Where technically available for your property.</span></div></div>
        <div class="check-item">{c}<div><strong>Energy &amp; retrofit information</strong><span>EPCs and retrofit recommendations, once available.</span></div></div>
      </div>
    </div>
  </div>
</section>
""".format(
        p1=icon("home", 15), p2=icon("document", 15), p3=icon("history", 15), p4=icon("camera", 15), p5=icon("layers", 15),
        c=icon("check", 18),
    )

    roadmap = """
<section class="section section--alt">
  <div class="container">
    <div class="section-head center">
      <span class="eyebrow">How We're Building This</span>
      <h2>The portal grows alongside the business</h2>
    </div>
    <div class="steps">
      <div class="step"><div class="step-num">1</div><div class="step-body"><h4>Phase 1 &mdash; today</h4><p>Professional website, services and enquiry process. No account system yet.</p></div></div>
      <div class="step"><div class="step-num">2</div><div class="step-body"><h4>Phase 2</h4><p>Structured quote and lead-tracking system behind the scenes.</p></div></div>
      <div class="step"><div class="step-num">3</div><div class="step-body"><h4>Phase 3</h4><p>Customer accounts, with reports, photographs and inspection history.</p></div></div>
      <div class="step"><div class="step-num">4</div><div class="step-body"><h4>Phases 4&ndash;6</h4><p>Mapping, 3D imagery and a full digital property intelligence record.</p></div></div>
    </div>
  </div>
</section>
"""

    content = hero + preview + roadmap + cta_band(
        prefix, "Want to be an early user of the Client Portal?", "Get in touch and we'll let you know as soon as customer accounts are available.",
        primary=("Contact Us", "contact.html"), secondary=("View Services", "services.html"),
    )

    write("portal.html", page(
        "portal", "Client Portal",
        "The PCT Property Intelligence Client Portal will bring together reports, photographs, inspection history and property information in one secure place.",
        content, prefix=prefix, active="",
    ))


# --------------------------------------------------------------------------
# RESOURCES
# --------------------------------------------------------------------------

RESOURCES_COMING_SOON = [
    "What is an EPC?",
    "What is a Retrofit Assessment?",
    "When is a drone inspection useful?",
    "What should you look for during a roof inspection?",
    "Why photographic property records are useful",
    "What should landlords keep records of?",
]

ARTICLE_CONTENT = {
    "how-often-should-gutters-be-cleaned": {
        "meta": "A practical guide to gutter cleaning frequency, warning signs of blockages, and why regular inspection matters.",
        "body": """
<p>Gutters do a quiet but important job: moving rainwater safely away from your roof, walls and foundations. When they're blocked, that water has to go somewhere else &mdash; often down external walls, into fascias, or pooling around foundations. The frustrating part is that a blocked gutter often isn't visible from ground level, so problems can build up unnoticed.</p>

<h2>How often should gutters actually be cleaned?</h2>
<p>As a general guide, most UK properties benefit from a gutter check at least twice a year &mdash; typically in spring and autumn. That said, the right frequency depends heavily on what's around the property:</p>
<ul>
  <li><strong>Properties near trees</strong>, especially overhanging deciduous trees, can need checking every few months during autumn leaf fall.</li>
  <li><strong>Properties with moss-prone roof coverings</strong> may see gutters fill with moss debris even without nearby trees.</li>
  <li><strong>Properties in more sheltered, tree-free locations</strong> may comfortably manage with an annual check.</li>
</ul>

<h2>Signs your gutters may need attention</h2>
<ul>
  <li>Visible sagging or pooling water in sections of the gutter.</li>
  <li>Plant growth or moss visible from ground level.</li>
  <li>Water marks or staining on external walls beneath the gutter line.</li>
  <li>Overflow during heavy rain, even where the gutter looks intact.</li>
</ul>

<h2>Why inspection matters as much as cleaning</h2>
<p>A clean gutter today doesn't tell you much about what it will look like in six months. That's why we treat inspection and cleaning as two separate, connected steps: inspection identifies blockages, moss, debris, overflow risk and any visible defects; cleaning then addresses what's found. PCT offers gutter inspection now, with gutter cleaning coming soon. Just as importantly, we document what we find with photographs, so you're shown the condition rather than simply told about it.</p>

<div class="report-note" style="margin-top:8px;"><strong>Related service</strong><p>See our <a href="../services/gutter-inspection-cleaning.html">Gutter Inspection &amp; Cleaning</a> service for more detail.</p></div>
""",
    },
    "what-can-a-drone-roof-inspection-identify": {
        "meta": "What aerial visual inspection can and can't tell you about your roof — and how it fits alongside other checks.",
        "body": """
<p>Roofs are one of the hardest parts of a property to inspect properly. Ground-level viewing only shows you certain angles, and access equipment like ladders or scaffolding can be slow, costly, and not always necessary just to have a look. A drone gives a safe, efficient way to see roof areas clearly &mdash; but it's worth understanding what that inspection can and can't tell you.</p>

<h2>What a drone roof inspection can identify</h2>
<ul>
  <li><strong>Visible surface condition</strong> &mdash; missing, slipped or damaged tiles and slates, visible cracking, and general wear.</li>
  <li><strong>Moss and debris build-up</strong> on roof surfaces and in valleys or gutters.</li>
  <li><strong>Visible flashing issues</strong> around chimneys, joints and roof penetrations.</li>
  <li><strong>General condition of chimneys and elevated features</strong> that are difficult to see from the ground.</li>
  <li><strong>Clear photographic evidence</strong> you can keep on file, refer back to, or share with contractors.</li>
</ul>

<h2>What it doesn't replace</h2>
<p>A drone inspection is a visual inspection. It provides condition observations and photographic evidence &mdash; it does not replace a structural survey, and it can't identify issues that aren't visible from the outside, such as problems with roof timbers, insulation, or ventilation inside the roof space. Where a finding suggests something more serious, the right next step is a referral to an appropriately qualified specialist.</p>

<h2>When it's most useful</h2>
<ul>
  <li>Before buying a property, as a supplement to (not a replacement for) a formal survey.</li>
  <li>After a storm, to check for obvious visible damage.</li>
  <li>As part of routine maintenance, to catch small issues before they become bigger ones.</li>
  <li>Alongside a Roof Inspection or Gutter Inspection, for a fuller picture in one visit.</li>
</ul>

<div class="report-note" style="margin-top:8px;"><strong>Related service</strong><p>See our <a href="../services/drone-inspection.html">Drone Inspection</a> service for more detail.</p></div>
""",
    },
    "what-is-a-property-inspection": {
        "meta": "An introduction to property inspection and documentation, and what to expect from a visit.",
        "body": """
<p>&ldquo;Property inspection&rdquo; covers a lot of ground &mdash; from a quick visual check to a detailed, documented review of a property's condition. At PCT, a property inspection means a structured visit focused on a clear goal: giving you accurate, well-organised information about your property, backed up with photographic evidence.</p>

<h2>What happens during an inspection visit</h2>
<ul>
  <li>A walkthrough of the areas relevant to what you've asked for &mdash; this might be the whole property, or a specific area like the roof or gutters.</li>
  <li>Photographs taken to document condition, using ground-level and, where useful, aerial techniques.</li>
  <li>Notes taken on anything observed, kept separate from any recommendations.</li>
</ul>

<h2>What you receive afterwards</h2>
<p>Every inspection results in a written summary and supporting photographs, organised so you can actually use the information &mdash; whether that's for your own records, a letting file, an insurance claim, or simply peace of mind. Findings are always presented as <strong>observations</strong> (what was seen) separately from <strong>recommendations</strong> (what may be worth investigating or doing next), so it's clear what's fact and what's guidance.</p>

<h2>What a property inspection isn't</h2>
<p>It isn't a structural survey, and it isn't a regulated specialist assessment such as an electrical or gas safety check. Where an inspection identifies something that needs specialist attention, the right step is a referral to an appropriately qualified professional &mdash; we're clear about that distinction throughout every report.</p>

<div class="report-note" style="margin-top:8px;"><strong>Related service</strong><p>See our <a href="../services/property-documentation.html">Property Documentation</a> service for more detail.</p></div>
""",
    },
}


def build_resources():
    prefix = ""
    hero = """
<section class="page-hero">
  <div class="container">
    {crumb}
    <span class="eyebrow">Resources</span>
    <h1>Property knowledge, explained clearly</h1>
    <p class="lede">Straightforward answers to common property, inspection and energy questions &mdash; no jargon, no unsupported claims.</p>
  </div>
</section>
""".format(crumb=breadcrumb(prefix, [("Home", "index.html"), ("Resources", None)]))

    live = """
<section class="section">
  <div class="container">
    <div class="grid grid-3">{cards}</div>
  </div>
</section>
""".format(cards="".join(resource_card(prefix, r) for r in RESOURCES))

    soon = """
<section class="section section--alt">
  <div class="container">
    <div class="section-head center">
      <span class="eyebrow">Coming Soon</span>
      <h2>More articles on the way</h2>
    </div>
    <div class="pill-list" style="justify-content:center;">
      {pills}
    </div>
  </div>
</section>
""".format(pills="".join('<span class="pill">%s</span>' % t for t in RESOURCES_COMING_SOON))

    content = hero + live + soon + cta_band(prefix, "Have a question we haven't covered?", "Ask us directly and we'll be glad to help.", primary=("Contact Us", "contact.html"), secondary=("View Services", "services.html"))

    write("resources.html", page(
        "resources", "Resources & Property Guides",
        "Practical, plain-language guides on property inspection, gutters, roofs and energy assessment from PCT Property Intelligence.",
        content, prefix=prefix, active="resources",
    ))


def build_resource_articles():
    for r in RESOURCES:
        prefix = "../"
        a = ARTICLE_CONTENT[r["slug"]]
        hero = """
<section class="page-hero">
  <div class="container">
    {crumb}
    <span class="eyebrow">{tag}</span>
    <h1>{title}</h1>
  </div>
</section>
""".format(crumb=breadcrumb(prefix, [("Home", "index.html"), ("Resources", "resources.html"), (r["title"], None)]), tag=r["tag"], title=r["title"])

        body = """
<section class="section">
  <div class="container">
    <div class="article-body">
      <div class="article-meta"><span>PCT Property Intelligence</span><span>&middot;</span><span>{tag}</span></div>
      {photo}
      {body}
    </div>
  </div>
</section>
""".format(tag=r["tag"], photo=photo(prefix, r["image"], r["alt"], cls="photo--rounded article-photo", sizes="(max-width: 760px) 100vw, 720px"), body=a["body"])

        content = hero + body + cta_band(prefix, "Want this checked on your own property?", "Request an assessment and we'll take it from here.")

        url = "%s/resources/%s.html" % (DOMAIN, r["slug"])
        schema = schema_tag({
            "@context": "https://schema.org",
            "@graph": [
                {
                    "@type": "Article",
                    "headline": r["title"],
                    "description": a["meta"],
                    "image": "%s/assets/img/%s-1600.jpg" % (DOMAIN, r["image"]),
                    "mainEntityOfPage": url,
                    "inLanguage": "en-GB",
                    "author": {"@type": "Organization", "name": "PCT Property Intelligence", "url": DOMAIN + "/"},
                    "publisher": {"@id": BUSINESS_ID, "@type": "Organization", "name": "PCT Property Intelligence",
                                  "logo": {"@type": "ImageObject", "url": DOMAIN + "/assets/img/logo-full-light.png"}},
                },
                breadcrumb_schema([("Home", ""), ("Resources", "resources.html"), (r["title"], "resources/%s.html" % r["slug"])]),
            ],
        })

        write("resources/%s.html" % r["slug"], page(
            "resources/" + r["slug"], r["title"], a["meta"], content, prefix=prefix, active="resources", schema=schema,
            og_type="article", og_image=r["image"],
        ))


# --------------------------------------------------------------------------
# LEGAL PAGES
# --------------------------------------------------------------------------

LEGAL_NOTE = (
    "<!-- Placeholder note for the business owner: insert company registration number "
    "(if a limited company) and ICO registration reference once obtained, before this "
    "page goes live. Do not publish fabricated registration details. -->"
)


def legal_shell(prefix, slug, eyebrow, title, updated, body):
    crumb = breadcrumb(prefix, [("Home", "index.html"), (title, None)])
    content = """
{note}
<section class="page-hero" style="padding-bottom:32px;">
  <div class="container">
    {crumb}
    <span class="eyebrow">{eyebrow}</span>
    <h1>{title}</h1>
  </div>
</section>
<section class="section">
  <div class="container">
    <div class="legal-body">
      <p class="legal-updated">Last updated: {updated}</p>
      {body}
    </div>
  </div>
</section>
""".format(note=LEGAL_NOTE, crumb=crumb, eyebrow=eyebrow, title=title, updated=updated, body=body)
    write(slug + ".html", page(
        slug, title, title + " for PCT Property Intelligence.", content, prefix=prefix, active="",
    ))


def build_privacy():
    body = """
<p>PCT Property Intelligence ("PCT", "we", "us", "our") is committed to protecting your privacy. This policy explains what personal information we collect through this website, how we use it, and the choices you have.</p>

<h2>Who we are</h2>
<p>PCT Property Intelligence is a property assessment, inspection and intelligence business operating in {area}. You can contact us about privacy matters at <a href="mailto:{email}">{email}</a>.</p>

<h2>What information we collect</h2>
<ul>
  <li><strong>Enquiry and quote form details</strong> &mdash; name, email, telephone number, property address and postcode, service requirements, preferred dates, and any details you choose to add.</li>
  <li><strong>Photographs</strong> you choose to send us relating to your property or enquiry.</li>
  <li><strong>Basic technical information</strong> &mdash; such as pages visited and general usage patterns, only where you have consented to analytics cookies. See our <a href="cookie-policy.html">Cookie Policy</a>.</li>
</ul>

<h2>How we use your information</h2>
<ul>
  <li>To respond to enquiries and provide quotes.</li>
  <li>To arrange, carry out and document assessments and inspections you book.</li>
  <li>To keep records associated with your property, where you become a customer.</li>
  <li>To meet legal, accounting and regulatory obligations.</li>
</ul>

<h2>Legal basis for processing</h2>
<p>We process your information on the basis of: taking steps at your request before entering into a contract (responding to enquiries and quotes); performing a contract with you (carrying out booked work); and our legitimate interests in running and improving our business, balanced against your rights.</p>

<h2>Sharing your information</h2>
<p>We do not sell your personal information. We may share information with trusted service providers who help us operate (for example, email or hosting providers), and where required by law.</p>

<h2>How long we keep your information</h2>
<p>We keep enquiry information for as long as reasonably necessary to respond to it, and customer and property records for as long as necessary to provide our services and meet legal obligations.</p>

<h2>Your rights</h2>
<p>Under UK data protection law, you have the right to access, correct, delete, or restrict the use of your personal information, and to object to certain processing. To exercise any of these rights, contact us at <a href="mailto:{email}">{email}</a>. You also have the right to complain to the Information Commissioner's Office (ICO) at ico.org.uk.</p>

<h2>Cookies</h2>
<p>This website uses cookies. See our <a href="cookie-policy.html">Cookie Policy</a> for full details and how to manage your preferences.</p>

<h2>Changes to this policy</h2>
<p>We may update this policy from time to time. The date at the top of this page shows when it was last revised.</p>
""".format(area=SERVICE_AREA, email=BUSINESS_EMAIL)
    legal_shell("", "privacy-policy", "Legal", "Privacy Policy", "September 2026", body)


def build_terms():
    body = """
<p>These terms apply to your use of this website and, where indicated, to the property assessment and inspection services provided by PCT Property Intelligence ("PCT", "we", "us", "our").</p>

<h2>Use of this website</h2>
<p>This website is provided for general information about PCT Property Intelligence and its services. While we aim to keep information accurate and up to date, we make no guarantee that content is complete, current, or free of error at all times.</p>

<h2>Enquiries and quotes</h2>
<p>Submitting an enquiry or quote request through this website does not create a binding contract. A booking is only confirmed once we have agreed scope, access and pricing directly with you.</p>

<h2>Nature of our services</h2>
<p>Our inspection and documentation services provide visual observations, photographic evidence and, where relevant, recommendations. They are not a substitute for a structural survey or other regulated specialist assessment (such as an electrical, gas, or roofing specialist opinion) unless expressly stated. Where a finding suggests a need for specialist assessment, we will say so.</p>

<h2>Drone operations</h2>
<p>Aerial inspection is carried out under a registered Flyer ID and Operator ID, in accordance with UK Civil Aviation Authority regulations. Flights are only carried out when conditions are safe and appropriate.</p>

<h2>Availability of services</h2>
<p>Some services referenced on this website are marked "Coming soon" and are not yet available. We do not accept bookings for services before they are genuinely available.</p>

<h2>Intellectual property</h2>
<p>The content, design and branding of this website belong to PCT Property Intelligence unless otherwise stated, and may not be reproduced without permission. Reports and photographs produced for a customer are provided for that customer's own use.</p>

<h2>Liability</h2>
<p>We take care in carrying out our services, but our reports reflect what was reasonably observable at the time of inspection using the methods described for that service. We are not liable for defects that were not visible or reasonably discoverable using those methods.</p>

<h2>Governing law</h2>
<p>These terms are governed by the law of England and Wales.</p>

<h2>Contact</h2>
<p>Questions about these terms can be sent to <a href="mailto:{email}">{email}</a>.</p>
""".format(email=BUSINESS_EMAIL)
    legal_shell("", "terms", "Legal", "Terms & Conditions", "September 2026", body)


def build_cookies():
    body = """
<p>This page explains how PCT Property Intelligence uses cookies on this website, and how you can manage your preferences.</p>

<h2>What are cookies?</h2>
<p>Cookies are small text files stored on your device that help websites function and, where permitted, help us understand how the site is used.</p>

<h2>Cookies we use</h2>
<table style="width:100%;border-collapse:collapse;margin:16px 0;font-size:0.92rem;">
  <thead><tr style="text-align:left;border-bottom:1px solid var(--line);">
    <th style="padding:10px 8px;">Type</th><th style="padding:10px 8px;">Purpose</th><th style="padding:10px 8px;">Consent required?</th>
  </tr></thead>
  <tbody>
    <tr style="border-bottom:1px solid var(--line-soft);"><td style="padding:10px 8px;">Essential</td><td style="padding:10px 8px;">Remembering your cookie preference, and basic site functionality.</td><td style="padding:10px 8px;">No &mdash; required for the site to work.</td></tr>
    <tr><td style="padding:10px 8px;">Analytics</td><td style="padding:10px 8px;">Understanding how visitors use the site, so we can improve it.</td><td style="padding:10px 8px;">Yes &mdash; only loaded after you accept.</td></tr>
  </tbody>
</table>

<h2>Managing your preference</h2>
<p>When you first visit, you'll be asked whether to accept analytics cookies. Analytics cookies are not loaded until you accept them. You can change your mind at any time by clearing your browser's site data for this website, which will show the preference banner again.</p>

<h2>Third-party cookies</h2>
<p>Where analytics are enabled, they may be provided by a third-party analytics service. We only use analytics data in aggregate to understand site usage &mdash; not to identify individuals.</p>

<h2>More information</h2>
<p>See our <a href="privacy-policy.html">Privacy Policy</a> for how we handle personal information more broadly, or contact us at <a href="mailto:{email}">{email}</a>.</p>
""".format(email=BUSINESS_EMAIL)
    legal_shell("", "cookie-policy", "Legal", "Cookie Policy", "September 2026", body)


def build_404():
    prefix = ""
    content = """
<section class="not-found">
  <div class="container">
    <span class="eyebrow" style="justify-content:center;">404</span>
    <h1 style="margin-top:14px;">We couldn't find that page</h1>
    <p class="lede" style="max-width:480px;margin:16px auto 32px;">The page may have moved, or the link may be out of date.</p>
    <div class="cta-row" style="justify-content:center;">
      <a class="btn btn-primary" href="index.html">Back to Homepage</a>
      <a class="btn btn-secondary" href="services.html">View Services</a>
    </div>
  </div>
</section>
"""
    write("404.html", page("404", "Page Not Found", "This page could not be found.", content, prefix=prefix, active="",
                           robots="noindex, follow"))


# --------------------------------------------------------------------------
# SITEMAP / ROBOTS
# --------------------------------------------------------------------------

def build_sitemap_robots():
    urls = ["", "about.html", "services.html", "contact.html", "resources.html", "portal.html",
            "privacy-policy.html", "terms.html", "cookie-policy.html"]
    urls += ["services/%s.html" % s["slug"] for s in SERVICES]
    urls += ["resources/%s.html" % r["slug"] for r in RESOURCES]

    import datetime
    today = datetime.date.today().isoformat()
    entries = "".join(
        "  <url><loc>%s/%s</loc><lastmod>%s</lastmod></url>\n" % (DOMAIN, u, today) for u in urls
    )
    sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n%s</urlset>\n' % entries
    write("sitemap.xml", sitemap)

    robots = "User-agent: *\nAllow: /\n\nSitemap: %s/sitemap.xml\n" % DOMAIN
    write("robots.txt", robots)


# --------------------------------------------------------------------------
# MAIN
# --------------------------------------------------------------------------

def main():
    build_home()
    build_about()
    build_services_overview()
    build_service_pages()
    build_contact()
    build_portal()
    build_resources()
    build_resource_articles()
    build_privacy()
    build_terms()
    build_cookies()
    build_404()
    build_sitemap_robots()
    print("\nDone. %d service pages, %d resource articles generated." % (len(SERVICES), len(RESOURCES)))


if __name__ == "__main__":
    main()
