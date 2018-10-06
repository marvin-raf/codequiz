import config from "../config";

const endpoint = url => {
  return `${config.host}${url}`;
};

export { endpoint };
