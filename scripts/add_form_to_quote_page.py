#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Add contact form from homepage to Get a Quote page
"""

from pathlib import Path

quote_page = Path("C:/Users/Spaceship/.openclaw/workspace/vinyl-website/get-a-quote.html")

# Contact form HTML from homepage
CONTACT_FORM_HTML = """
<section id="contact" style="padding:80px 0;background:var(--surface);border-top:1px solid var(--border);">
  <div class="container">
    <div class="contact-grid">
      <div class="contact-info">
        <span class="section-label">Get In Touch</span>
        <h2 class="section-title">Get a Free Quote</h2>
        <p style="color:var(--muted);font-size:15px;margin:20px 0 40px;line-height:1.75;">
          Fill out the form and we'll get back to you within 24 hours with a quote. Prefer to talk? Give us a call.
        </p>
        <div class="contact-detail">
          <div class="icon">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07A19.5 19.5 0 0 1 4.69 12a19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 3.6 1.2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L7.91 8.8a16 16 0 0 0 6 6l.91-1a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 21.5 16z"/></svg>
          </div>
          <div>
            <div class="dl">Phone</div>
            <div class="dv"><a href="tel:3038824656">303-882-4656</a></div>
          </div>
        </div>
        <div class="contact-detail">
          <div class="icon">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg>
          </div>
          <div>
            <div class="dl">Email</div>
            <div class="dv"><a href="mailto:highcountryfinishandrepairco@gmail.com">highcountryfinishandrepairco@gmail.com</a></div>
          </div>
        </div>
        <div class="contact-detail">
          <div class="icon">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>
          </div>
          <div>
            <div class="dl">Service Area</div>
            <div class="dv">Denver & surrounding areas (1hr radius)</div>
          </div>
        </div>
      </div>
      <div>
        <div class="quote-form">
          <h3 style="font-size:26px;margin-bottom:28px;">Request a Free Quote</h3>
          <form id="quote-form" action="https://formspree.io/f/mqeydnkg" method="POST">
            <div class="form-row">
              <div class="form-group">
                <label>First Name *</label>
                <input type="text" name="first_name" required/>
              </div>
              <div class="form-group">
                <label>Last Name *</label>
                <input type="text" name="last_name" required/>
              </div>
            </div>
            <div class="form-row">
              <div class="form-group">
                <label>Phone *</label>
                <input type="tel" name="phone" required/>
              </div>
              <div class="form-group">
                <label>Email *</label>
                <input type="email" name="email" required/>
              </div>
            </div>
            <div class="form-group">
              <label>Service Needed *</label>
              <select name="service" required>
                <option value="" disabled selected>Select a service...</option>
                <option>Vehicle Wrap (Full)</option>
                <option>Vehicle Wrap (Partial)</option>
                <option>Spot Graphics / Decals</option>
                <option>Window Tint - Residential</option>
                <option>Window Tint - Commercial</option>
                <option>Frosted / Decorative Window Film</option>
                <option>Lobby / Reception Sign</option>
                <option>Stand-Off / Dimensional Sign</option>
                <option>Building / Fascia Sign</option>
                <option>Office / Suite Sign</option>
                <option>Wall Graphic / Mural</option>
                <option>Multiple Services</option>
                <option>Not Sure - Need Consultation</option>
              </select>
            </div>
            <div class="form-group">
              <label>Project Details</label>
              <textarea name="message" placeholder="Tell us about your project — vehicle type, dimensions, timeline, any specific requirements..."></textarea>
            </div>
            <button type="submit" class="form-submit">Send My Quote Request →</button>
            <p class="form-note">We respond within 24 hours. No spam, ever.</p>
          </form>
          <div class="form-success" id="form-success">
            ✓ Message received!<br/>
            <span style="font-size:15px;font-family:Inter,sans-serif;color:var(--muted)">We'll be in touch within 24 hours.</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>
"""

# Form CSS
FORM_CSS = """
/* ─── CONTACT FORM ────────────────────────── */
#contact { background: var(--black); }

.contact-grid {
  display: grid;
  grid-template-columns: 1fr 1.4fr;
  gap: 80px;
  align-items: start;
}

.contact-info { padding-top: 8px; }

.contact-detail {
  display: flex;
  align-items: flex-start;
  gap: 16px;
  margin-bottom: 28px;
}

.contact-detail .icon {
  width: 40px;
  height: 40px;
  border: 1px solid var(--border);
  border-radius: 2px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  color: var(--gold);
}

.contact-detail .dl { font-size: 11px; text-transform: uppercase; letter-spacing: 1.5px; color: var(--muted); margin-bottom: 4px; }
.contact-detail .dv { font-size: 15px; font-weight: 500; color: var(--text); }
.contact-detail .dv a:hover { color: var(--gold); }

.quote-form {
  background: var(--surface);
  padding: 48px;
  border: 1px solid var(--border);
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  font-size: 11px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 1.5px;
  color: var(--muted);
  margin-bottom: 8px;
}

.form-group input,
.form-group select,
.form-group textarea {
  width: 100%;
  background: var(--black);
  border: 1px solid var(--border);
  color: var(--text);
  padding: 13px 16px;
  font-size: 14px;
  font-family: 'Inter', sans-serif;
  border-radius: 2px;
  outline: none;
  transition: border-color .2s;
  appearance: none;
}

.form-group input:focus,
.form-group select:focus,
.form-group textarea:focus { border-color: var(--gold); }

.form-group textarea { resize: vertical; min-height: 120px; }
.form-group select { cursor: pointer; }

.form-submit {
  width: 100%;
  background: var(--gold);
  color: #000;
  border: none;
  padding: 16px;
  font-size: 13px;
  font-weight: 700;
  letter-spacing: 1.5px;
  text-transform: uppercase;
  cursor: pointer;
  border-radius: 2px;
  font-family: 'Inter', sans-serif;
  transition: background .2s;
  margin-top: 8px;
}

.form-submit:hover { background: var(--gold-light); }

.form-note { font-size: 12px; color: var(--muted); margin-top: 12px; text-align: center; }

.form-success {
  display: none;
  padding: 32px;
  background: rgba(201,168,76,.08);
  border: 1px solid var(--gold);
  border-radius: 4px;
  text-align: center;
  font-size: 18px;
  font-weight: 600;
  color: var(--gold);
  margin-top: 24px;
}

@media(max-width:768px) {
  .contact-grid { grid-template-columns: 1fr; gap: 48px; }
  .quote-form { padding: 32px 24px; }
  .form-row { grid-template-columns: 1fr; }
}
"""

# Form JavaScript
FORM_JS = """
// Quote form submission
document.getElementById('quote-form').addEventListener('submit', async(e) => {
  e.preventDefault();
  const form = e.target;
  const btn = form.querySelector('.form-submit');
  const originalText = btn.textContent;
  
  btn.textContent = 'Sending...';
  btn.disabled = true;
  
  try {
    const res = await fetch(form.action, {
      method: 'POST',
      body: new FormData(form),
      headers: { 'Accept': 'application/json' }
    });
    
    if (res.ok) {
      form.style.display = 'none';
      document.getElementById('form-success').style.display = 'block';
    } else {
      throw new Error('Form submission failed');
    }
  } catch (err) {
    btn.textContent = originalText;
    btn.disabled = false;
    alert('Something went wrong. Please call us at 303-882-4656.');
  }
});
"""

# Read current get-a-quote.html
with open(quote_page, 'r', encoding='utf-8') as f:
    content = f.read()

# Add form CSS before </style>
if '/* ─── CONTACT FORM' not in content:
    style_end = content.find('</style>')
    if style_end != -1:
        content = content[:style_end] + '\n' + FORM_CSS + '\n' + content[style_end:]

# Add form HTML before footer
if '<section id="contact"' not in content:
    footer_start = content.find('<footer>')
    if footer_start != -1:
        content = content[:footer_start] + CONTACT_FORM_HTML + '\n' + content[footer_start:]

# Add form JavaScript before closing </script>
if 'quote-form' not in content:
    # Find last </script> before </body>
    body_end = content.rfind('</body>')
    if body_end != -1:
        # Find last </script> before body end
        script_end = content.rfind('</script>', 0, body_end)
        if script_end != -1:
            content = content[:script_end] + '\n' + FORM_JS + '\n' + content[script_end:]

# Write back
with open(quote_page, 'w', encoding='utf-8') as f:
    f.write(content)

print("Added contact form to Get a Quote page")
print("- Form HTML added before footer")
print("- Form CSS added to stylesheet")
print("- Form JavaScript added for submission handling")
