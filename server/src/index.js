import express from 'express'
import 'dotenv/config'

const app = express
const port = process.env.PORT || 3000

app.get('/home',(req, res)=>{
    res.send('<h1>Hello world</h1>')
})

app.listen