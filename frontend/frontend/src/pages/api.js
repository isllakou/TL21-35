import axios from "axios";
import PassesPerStation from "./PassesPerStation";

// axios.default.baseURL = 'http://127.0.0.1:9103/interoperability/api/';

const API_URL = 'http://127.0.0.1:9103/interoperability/api/';

class User {
    generateInfo(obj) {
      return axios.get(API_URL+'PassesPerStation/' + obj.station + '/' + obj.datefrom + '/'+ obj.dateto);
    }
}
// export const generateInfo = obj => {
//     const stationlist = 'PassesPerStation/' + obj.station + '/' + obj.datefrom + '/'+ obj.dateto ;
// 	return axios.get(stationlist);
// }; 

// generateInfo() {
//     return axios.get(API_URL + 'user', { headers: authHeader() });
//   };

export default new User();
