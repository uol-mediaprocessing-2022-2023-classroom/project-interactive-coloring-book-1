<template>
  <v-container>
    <div class="selectedImageField">
      <div class="selectedImageContainer">
        <div class="loginField">
          <div style="display: flex" v-if="isUserNameEmpty">
            <input
              required
              placeholder="Email"
              v-model="loginData.email"
              type="email"
              name="email"
              autocomplete="email"
            />
            <input
              required
              placeholder="Password"
              v-model="loginData.password"
              type="password"
              name="password"
              autocomplete="password"
            />
          </div>
          <h1 v-if="!isUserNameEmpty" style="margin-right: 15px">
            {{ this.userName }}
          </h1>
          <v-btn
            class="clickable loginBtn"
            :disabled="awaitingLoginResponse"
            color="#d6d8e4"
            @click="login"
          >
            <v-progress-circular
              indeterminate
              color="grey lighten-5"
              v-if="awaitingLoginResponse"
            ></v-progress-circular>
            <div style="display: flex" v-else>
              {{ this.loginButtonText }}
            </div>
          </v-btn>
        </div>

        <div class="selectedImageInfo">
          <h2>Selected Image: <br /></h2>
        </div>

        <div style="display: flex">
            <div class="flexImg">
                <img class="selectedImg" v-bind:src="selectedImage.url" />
            </div>
            <div class="inputField">
                <input placeholder="Your CEWE cldID"
                       class="idInput"
                       v-model="cldId" />
                <!-- Simple button that calls the method 'loadImages' -->
                <button class="basicButton" @click="loadImages(cldId)">
                    Load Images
                </button>

                <br>

                <!-- slider for difficulty level -->
                <v-slider v-model="difficulty"
                          label="Difficulty"
                          :max="3"
                          :min="1"
                          :thumb-size="24"
                          thumb-label="always"
                          step="1"
                          ticks>
                </v-slider>

                
                <v-btn
            class="basicButton"
            :disabled="awaitingResponse"
            color="#d6d8e4"
            @click="getSegments(selectedImage.id)"
          >
            <v-progress-circular
              indeterminate
              color="grey lighten-5"
              v-if="awaitingResponse"
            ></v-progress-circular>
            <div style="display: flex" v-else>
              {{ 'Apply Segmentation' }}
            </div>
          </v-btn>

                <div>
                    <h3>Image Info:<br /></h3>
                    <p>
                        {{ imageInfo.name }}
                    </p>
                    <p>
                        {{ imageInfo.avgColor }}
                    </p>
                </div>
            </div>
        </div>
      </div>
    </div>

    <div class="imageGalleryField">
      <div>
        <v-row>
          <v-col
            v-for="n in galleryImageNum"
            :key="n"
            class="d-flex child-flex"
            cols="2"
          >
            <v-img
              :src="currGallery[n - 1].url"
              aspect-ratio="1"
              max-height="200"
              max-width="200"
              class="grey lighten-2"
              @click="updateSelected(currGallery[n - 1].id)"
            >
              <template v-slot:placeholder>
                <v-row class="fill-height ma-0" align="center" justify="center">
                  <v-progress-circular
                    indeterminate
                    color="grey lighten-5"
                  ></v-progress-circular>
                </v-row>
              </template>
            </v-img>
          </v-col>
        </v-row>
      </div>
      <button class="loadMoreBtn" @click="$emit('loadMore')">Load more</button>
    </div>
  </v-container>
</template>

<script>

export default {
  name: "HomePage",

  data() {
    return {
      cldId: "",
      userName: "",
      loginData: { email: "", password: "" },
      imageInfo: { name: "", avgColor: "" },
      awaitingLoginResponse: false,
      loginButtonText: "LOGIN",
      isLoggedIn: false,
      difficulty: "1",
     
    };
  },

  props: {
      selectedImage: Object,
    currGallery: Array,
    awaitingResponse: Boolean,
  },

  methods: {
    /*
      Emit a loadImages event.
    */
    loadImages() {
      console.log(this.awaitingResponse)
      this.$emit("loadImages", this.cldId);
    },

    /*
      Emit a updateSelected event with the ID of the selected image.
      This method is called when the user clicks/selects an image in the gallery of loaded images.

      @param selectedId The ID of the selected image.
    */
    updateSelected(selectedId) {
      this.$emit("updateSelected", selectedId, this.cldId);
    },

    /*
      Emit a getBlur event with the ID of the selected image.
        
      @param selectedId The ID of the selected image.
    */
      getSegments(selectedId) {
        console.log(this.awaitingResponse)
          this.$emit("getBlur", selectedId, this.cldId, this.difficulty);
    },

    /*
      Send a login request to the CEWE API test server.
      If the user is already logged in, send a logout request instead.
    */
    async login() {
      if (this.isLoggedIn) {
        this.logout();
        return;
      }

      if (this.awaitingLoginResponse) {
        return;
      }
      this.awaitingLoginResponse = true;

      let loginData = this.loginData;
      const requestOptions = {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          clientVersion: "0.0.1-medienVerDemo",
          apiAccessKey: "6003d11a080ae5edf4b4f45481b89ce7",
        }, // this apiAccessKey is for testing
        body: JSON.stringify({
          login: loginData.email,
          password: loginData.password,
          deviceName: "Medienverarbeitung CEWE API Demo",
        }),
      };

      let status = 0;
      const response = await fetch(
        "https://cmp.photoprintit.com/api/account/session/",
        requestOptions
      ).then((response) => {
        status = response.status;

        if (!(status >= 200 && status <= 299)) {
          this.awaitingLoginResponse = false;
          // some broad status 'handling'
          if (status == 500 || status == 405) {
            alert("Internal error occured, try again later.");
            return;
          }
          alert("Entered credinentials are incorrect.");
          return;
        }

        this.awaitingLoginResponse = false;
        return response.json();
      });

      if(response == null){
        return;
      }

      let cldId = response.session.cldId;
      let userName = response.user.firstname;
      this.loginData = {
        email: "",
        password: "",
      };

      this.loggedIn(cldId, userName);
    },

    // Helper method called by login(), logs out the user.
    // Also resets saved website data.
    async logout() {
      if (!this.isLoggedIn) {
        return;
      }

      const requestOptions = {
        method: "DELETE",
        headers: { cldId: this.cldId, clientVersion: "0.0.1-offismosaic" },
      };

      const response = await fetch(
        "https://cmp.photoprintit.com/api/account/session/?invalidateRefreshToken=true",
        requestOptions
      );
      const status = response.status;
      if (!(status >= 200 && status <= 299)) {
        alert("Something went wrong during logout.");
        this.loggedOut();
        return;
      }

      this.loggedOut();
    },

    // Helper method for saving user data in the browsers local storage.
    loggedIn(cldId, userName) {
      this.cldId = cldId;
      this.isLoggedIn = true;
      this.userName = userName;
      localStorage.cldId = cldId;
      localStorage.userName = userName;
      localStorage.isLoggedIn = true;
    },

    // Helper method for clearing user data from the browsers local storage.
    loggedOut() {
      localStorage.cldId = "";
      localStorage.userName = "";
      localStorage.isLoggedIn = false;
      this.resetData();
    },

    // Helper method for resetting saved data.
    resetData() {
      this.cldId = "";
      this.isLoggedIn = false;
      this.userName = "";
      this.loginData = { email: "", password: "" };
      this.imageInfo = { name: "", avgColor: "" };
      this.awaitingLoginResponse = false;
      this.$emit("resetGalery");
    },
  },

  computed: {
    /*
        The numer of images within currGallery can dynamically change after the DOM is loaded, since the size of the image gallery depends on it
        it's important for it to be updated within the DOM aswell. By using computed values this is not a problem since Vue handles any updates to such
        values and updates them in the DOM.
        */
    galleryImageNum() {
      return this.currGallery.length;
    },

    isUserNameEmpty: function () {
      return this.userName == "";
    },
  },

  watch: {
    /*
      Watcher function for updating the displayed image information.
    */
    selectedImage: function () {
      this.imageInfo = {
        name: "Name: " + this.selectedImage.name,
        avgColor: "Average color: " + this.selectedImage.avgColor,
      };
    },

    /*
      Watcher function for updating login button text.
    */
    isLoggedIn(isLoggedIn) {
      if (isLoggedIn) {
        this.loginButtonText = "LOGOUT";
      } else {
        this.loginButtonText = "LOGIN";
      }
    },
  },

  mounted() {
    // Load from local storage
    if (localStorage.isLoggedIn === "true") {
      this.cldId = localStorage.cldId;
      this.userName = localStorage.userName;
      this.isLoggedIn = true;
    }
  },
};
</script>

<style scoped>
.selectedImageField {
  display: flex;
  flex-direction: row;

  background-color: rgb(249, 251, 255);
  border-radius: 10px;
  box-shadow: 0 10px 10px 10px rgba(0, 0, 0, 0.1);
  color: black;

  padding: 1%;
}

.imageGalleryField {
  display: flex;
  flex-direction: column;

  background-color: rgb(249, 251, 255);
  border-radius: 10px;
  box-shadow: 0 10px 10px 10px rgba(0, 0, 0, 0.1);
  color: black;

  padding: 1%;
  margin-top: 1%;
  max-height: 600px;
  overflow-y: auto;
}

.selectedImg {
  max-width: 500px;
  max-height: 500px;
}

.paletteImg {
  max-width: 500px;
  max-height: 50px;
}

.selectedImageInfo {
  margin-left: 10px;
}

.basicButton {
  background-color: rgb(226, 215, 215);
  padding: 0px 4px 0px 4px;
  margin-right: 5px;
  border-radius: 3px;
  width: 200px;
}

.flexImg {
    display: flex;
    flex-direction: column;
}

.idInput {
  margin-right: 8px;
  border: 1px solid #000;
  border-radius: 3px;
}

.loginField {
  display: flex;
  margin-left: auto;
  margin-bottom: 12px;
}

.loginField * {
  margin: 0px 5px 0px 5px;
}

.loginField * input {
  border: 1px solid #000;
  border-radius: 3px;
}

.inputField {
  display: flex;
  flex-direction: column;
  margin-left: 10px;
  width: 400px;
}

.inputField * {
  margin: 5px 0px 5px 0px;
}

.loadMoreBtn {
  background-color: #a7a7a7;
  border-radius: 6px;
  padding-left: 5px;
  padding-right: 5px;
  width: 100px;
  align-self: center;
  margin-top: 10px;
}
</style>