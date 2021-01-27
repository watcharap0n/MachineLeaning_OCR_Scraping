{% extends "template_fastapi/layout.html" %}
{% block content %}
  <br>
  <br>
  <div id="app">
    <v-app id="inspire">
      <br>
      <br>
      <br>
      <div class="jumbotron">
        <v-container>
          <v-card
              class="mx-auto"
              width="100%"
          >
            <v-row jusitfy="center">
              <v-col
                  small="6"
                  cols="6">

                <v-carousel
                    width="100%"
                    height="100%"
                    cycle
                    hide-delimiter-background
                    show-arrows-on-hover
                >
                  <v-carousel-item
                      v-for="(item,i) in items"
                      :key="i"
                      :src="item.src"
                  ></v-carousel-item>
                </v-carousel>

              </v-col>
              <v-col
                  cols="6"
                  small="6"
              >
                <div class="text-center" style="font-family: 'Balsamiq Sans', cursive;">
                  <h2> Welcome </h2>
                  <h6> Please Sign In</h6>
                  <v-container>
                    <v-form
                        v-model="valid"
                        ref="form"
                        lazy-validation
                    >
                      <v-text-field
                          :rules="validEmail"
                          v-model="formElement.username"
                          class="rounded-pill"
                          outlined
                          clearable
                          label="Username"
                          required
                      ></v-text-field>


                      <v-text-field
                          :rules="validOther"
                          v-model="formElement.password"
                          class="rounded-pill"
                          outlined
                          clearable
                          label="Password"
                          required
                      ></v-text-field>

                      <v-checkbox
                          style="margin-top: -10px; margin-bottom: 10px"
                          v-model="formElement.checkbox"
                          label="remember"
                          color="red"
                          value="checked"
                          hide-details
                      ></v-checkbox>

                      <v-btn block
                             :disabled="!valid"
                             color="red"
                             class="mr-4 rounded-pill text-white"
                             @click="login"
                      >
                        ยืนยัน
                      </v-btn>
                    </v-form>
                    <div class="text-center" style="margin-top: 20px">
                      <p>
                        Dont' have an account? <a href="/signin">Sign In</a>
                      </p>
                      <p>
                        <a href="/forgot">
                          Forgot Password
                        </a>
                      </p>
                    </div>
                  </v-container>
                </div>
              </v-col>

            </v-row>
          </v-card>
        </v-container>
      </div>
    </v-app>
  </div>


  <script>

      new Vue({
          el: '#app',
          vuetify: new Vuetify(),
          data: () => ({
              validEmail: [
                  v => !!v || 'Invalid Username',
                  v => /.+@.+\..+/.test(v) || 'Please input your email valid',
              ],
              validOther: [v => !!v || 'Invalid password'],
              valid: false,
              formElement: {
                  username: '',
                  password: '',
                  checkbox: []
              },
              items: [
                  {
                      src: '/static/images/iot1.png'
                  },
                  {
                      src: '/static/images/41002.jpg',
                  }
              ],
          }),
          methods: {
              login() {
                  let form = this.$refs.form.validate();
                  if (form === true) {
                      const path = '/login'
                      axios.post(path, this.formElement)
                          .then((res) => {
                              console.log(res)
                              console.log('success')
                          })
                          .catch((err) => {
                              console.error(err)
                          })
                  } else {
                      console.log('error')
                  }
              }
          },
          delimiters: ["[[", "]]"]
      })
  </script>



{% endblock %}