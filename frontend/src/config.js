const config = {};

config.host = process.env.NODE_ENV === "production"
                  ? "https://api.codequiz.co.nz"
                  : "http://localhost:5000";
export default config;