var path = require("path");
var webpack = require("webpack");
require("babel-polyfill");
var WebpackBundleAnalyzer =
    require("webpack-bundle-analyzer").WebpackBundleAnalyzer;

const distPath = process.env.NODE_ENV === "production" ? "../frontend-serve/dist" : "dist";

module.exports = {
    entry : [ "babel-polyfill", "./src/main.js" ],
    output : {
        path : path.resolve(__dirname, distPath),
        publicPath : distPath,
        filename : "build.js"
    },
    module : {
        rules : [
            {test : /\.css$/, use : [ "vue-style-loader", "css-loader" ]}, {
                test : /\.scss$/,
                use : [ "vue-style-loader", "css-loader", "sass-loader" ]
            },
            {
                test : /\.sass$/,
                use : [
                    "vue-style-loader", "css-loader",
                    "sass-loader?indentedSyntax"
                ]
            },
            {
                test : /\.vue$/,
                loader : "vue-loader",
                options : {
                    loaders : {
                        // Since sass-loader (weirdly) has SCSS as its default
                        // parse mode, we map
                        // the "scss" and "sass" values for the lang attribute
                        // to the right configs here.
                        // other preprocessors should work out of the box, no
                        // loader config like this necessary.
                        scss :
                            [ "vue-style-loader", "css-loader", "sass-loader" ],
                        sass : [
                            "vue-style-loader", "css-loader",
                            "sass-loader?indentedSyntax"
                        ]
                    }
                    // other vue-loader options go here
                }
            },
            {test : /\.js$/, loader : "babel-loader", exclude : /node_modules/},
            {
                test : /\.(png|jpg|gif|svg)$/,
                loader : "file-loader",
                options : {name : "[name].[ext]?[hash]"}
            }
        ]
    },
    resolve : {
        alias : {vue$ : "vue/dist/vue.esm.js"},
        extensions : [ "*", ".js", ".vue", ".json" ]
    },
    devServer : {historyApiFallback : true, noInfo : true, overlay : true},
    performance : {hints : false},
    devtool : "#eval-source-map"
};

if (process.env.NODE_ENV === "production") {
    module.exports.devtool = "#source-map";
    // http://vue-loader.vuejs.org/en/workflow/production.html
    module.exports.plugins = (module.exports.plugins || []).concat([
        // new WebpackBundleAnalyzer({}),
        new webpack.DefinePlugin({"process.env" : {NODE_ENV : '"production"'}}),
        new webpack.optimize.UglifyJsPlugin(
            {sourceMap : true, compress : {warnings : false}}),
        new webpack.LoaderOptionsPlugin({minimize : true})
    ]);
}
