const express = require("express");
const path = require("path");
const app = express();

app.use("/dist", express.static(__dirname + '/dist'));

app.get("*", (req, res) =>  {
  res.sendFile(path.resolve(__dirname, 'index.html'));
});

app.listen(9002, () =>  {
  console.log("listening on port 9002");
});
