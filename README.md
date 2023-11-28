# Getting a pulse of the housing market in Switzerland


## API Documentation

In browser:

`<host>:<port>/redoc`

## Web Scraping

Web scraping can be performed by using a Browser Driver in headless mode, using tools
like Selenium, Puppeteer or Playwright. 

But it should also always be possible to get all the data you need using only requests,
even for dynaminc websites using lots of JavaScript.

See: https://betterprogramming.pub/how-to-scrape-modern-websites-without-headless-browsers-d871bbd1119e

- In Chrome, open the _developer tools_ view.
- Make the request by clicking somewhere in the website
- Check the url(s) that were called in the _Network_ tab of the developer tools.

### Using a HTTP/S WebProxy

- https://medium.com/better-practices/reverse-engineering-an-api-403fae885303
  - https://mitmproxy.org/

### Cloudflare captach

- https://www.reddit.com/r/webscraping/comments/15l20ww/cloudflare_captcha_loop/
  - Connect playwright/puppeteer to regular chrome browser
    - https://stackoverflow.com/questions/71362982/is-there-a-way-to-connect-to-my-existing-browser-session-using-playwright

## Resources

- https://github.com/dvdblk/swiss-immo-scraper
- https://github.com/charnley/no-place-like-tilde
- https://github.com/denysvitali/homegate-rs
