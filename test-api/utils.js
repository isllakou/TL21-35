import axios from "axios";

// export const BASE_URL = "https://jsonplaceholder.typicode.com";
export const URL = 'http://127.0.0.1:9103/interoperability/api';

export const fetchPassesPerStation = async () => {
  try {
    return await axios.get(`${BASE_URL}/PassesPerStation/NE01/20000102/20210102`);
  } catch (e) {
    return [];
  }
};
  
  jest.mock("axios");
  
  describe("fetchPassesPerStation", () => {
    describe("when API call is successful", () => {
      it("should return passes list", async () => {
        // // given
        // const users = [
        //   { id: 1, name: "John" },
        //   { id: 2, name: "Andrew" },
        // ];
        // axios.get.mockResolvedValueOnce(users);
  
        // when
        const result = await fetchPassesPerStation();
  
        // then
        expect(axios.get).toHaveBeenCalledWith(`${BASE_URL}/PassesPerStation/NE01/20000102/20210102`);
        // expect(result).toEqual(users);
      });
    });
  
    // describe("when API call fails", () => {
    //   it("should return empty users list", async () => {
    //     // given
    //     const message = "Network Error";
    //     axios.get.mockRejectedValueOnce(new Error(message));
  
    //     // when
    //     const result = await fetchPassesPerStation();
  
    //     // then
    //     expect(axios.get).toHaveBeenCalledWith(`${BASE_URL}/PassesPerStation/NE01/20000102/20210102`);
    //     expect(result).toEqual([]);
    //   });
    // });
  });