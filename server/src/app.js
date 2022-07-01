import express from 'express'
import cors from 'cors'
import cookieParser from 'cookie-parser'
import 'dotenv/config'

const app = express()
app.use(cors())
app.use(express.json())
app.use(cookieParser())
const port = process.env.PORT || 3001

app.get('/home',(req, res)=>{
    res.send('<h1>Hello world</h1>')
})
app.listen(port, ()=>{
    console.log(`Server up and running on ${port}`)
})
