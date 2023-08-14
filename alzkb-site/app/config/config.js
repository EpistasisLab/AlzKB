const config = {
  dev: {
    neo_browser: 'http://' + process.env.ALZKB_NEO4J_BROWSER + ':' + process.env.ALZKB_NEO4J_BROWSER_HTTP_PORT + '/browser/',
  },
  prod: {
    neo_browser: 'https://' + process.env.ALZKB_NEO4J_BROWSER + '/browser/'
  }
}

if (process.env.NODE_ENV === "prod") {
  module.exports = config.prod
} else {
  module.exports = config.dev
}
