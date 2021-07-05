const express = require('express')
const app = express()
const port = 3000

app.get('/', (req, res) => {
    res.json('OvO server')
})

app.listen(port, () => {
    console.log(`OvO server now listening at http://localhost:${port}`)
})