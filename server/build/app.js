"use strict";

var _interopRequireDefault = require("@babel/runtime/helpers/interopRequireDefault");

var _express = _interopRequireDefault(require("express"));

require("dotenv/config");

var app = (0, _express["default"])();
var port = process.env.PORT || 3001;
app.get('/home', function (req, res) {
  res.send('<h1>Hello world</h1>');
});
app.listen(port, function () {
  console.log("Server up and running on ".concat(port));
});
//# sourceMappingURL=app.js.map