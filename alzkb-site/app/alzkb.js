const express = require('express')
require('dotenv').config()
// const path = require('path')
const config = require('./config/config')

const app = express()
const cors = require('cors')
const compression = require('compression')
// const helmet = require('helmet')
// const ejs = require('ejs')
require('ejs')

app.use(cors())
app.use(compression())
app.use(express.static('public', { maxAge: 3600000 }))
app.set('view engine', 'ejs')
// app.use(helmet())

app.get('/', (req, res) => {
  res.render('alzkb', config)
})

app.get('/about', (req, res) => {
  res.render('about', config)
})

app.get('/alzkb', (req, res) => {
  res.render('alzkb_about')
})

app.get('/samples', (req, res) => {
  res.render('samples')
})

app.listen(process.env.ALZKB_PORT, () => {
  console.log("port", process.env.ALZKB_PORT)
})
