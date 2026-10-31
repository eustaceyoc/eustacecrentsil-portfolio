# eustacecrentsil.vercel.app

This is my personal website and portfolio. It has my services, my resume, case studies for client projects, and case studies for the sample sites I made for local service businesses.

Live: https://eustacecrentsil.vercel.app

## Stack

Plain HTML, CSS and JavaScript. No framework and no build step. It's hosted on Vercel.

The contact form posts to Formspree.

## Running it locally

Open `index.html` in a browser, or serve the folder:

```
npx serve .
```

Then go to the address it prints (usually http://localhost:3000). Serving it is better than opening the file directly, because links like `/work/...` need a server.

## Layout

- `index.html` is the home page
- `services/` is the services page
- `work/` is the portfolio page, and `work/<project>/` holds one case study per project, with its screenshots and share image
- `404.html` is the not-found page
- `vercel.json` turns on trailing slashes, so `/work/x` redirects to `/work/x/`
- `sitemap.xml` and `robots.txt` are for search engines
- `Eustace-Crentsil-CV.pdf` is my CV
- `source/` has the page template and small Python scripts I used to make edits. The live site doesn't need them.
