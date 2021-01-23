{% extends "layout.html" %}
{% block content %}
  <br>
  <br>
  <br>
  <div class="text-center"><h2>OCR TO FORM</h2></div>
  <div id="app">
    <div class="container">

      <v-app id="inspire">
        <v-container>
          <v-row justify="center">
            <v-col
                cols="12"
                sm="10"
                md="8"
                lg="6"
            >
              <v-card>
                <v-form
                    ref="form"
                    lazy-validation
                >
                  <v-card-text>
                    <v-file-input
                        dense
                        outlined
                        clearable
                        label="รูปภาพแปลงเป็๋นข้อความ"
                        required
                        prepend-icon="mdi-camera"
                        ref="file"
                        v-model="files"
                    >
                      <v-btn
                          :loading="!spinner"
                          @click="postData"
                          x-small
                          slot="append"
                          color="green"
                      >
                        <v-icon
                            color="white"
                        >
                          mdi-clipboard-text-outline
                        </v-icon>
                      </v-btn>
                    </v-file-input>

                    <v-text-field
                        dense
                        outlined
                        clearable
                        label="Company"
                        v-model="form.company"
                        required
                    ></v-text-field>
                    <v-text-field
                        dense
                        outlined
                        clearable
                        v-model="form.tax_id"
                        label="Tax ID"
                        required
                    ></v-text-field>

                    <v-text-field
                        dense
                        outlined
                        clearable
                        v-model="form.date"
                        label="DATE"
                        required
                    ></v-text-field>

                    <v-row>
                      <v-col cols="6">
                        <v-textarea
                            dense
                            outlined
                            clearable
                            v-model="form.list_1"
                            label="List"
                            required
                        ></v-textarea>
                      </v-col>
                      <v-col cols="6">
                        <v-textarea
                            dense
                            outlined
                            clearable
                            v-model="form.pro_1"
                            label="Promotion"
                            required
                        ></v-textarea>
                      </v-col>
                    </v-row>
                    <v-text-field
                        dense
                        outlined
                        clearable
                        v-model="form.price_1"
                        label="Each List"
                        required
                    ></v-text-field>

                    <v-text-field
                        v-model="form.price_2"
                        dense
                        outlined
                        clearable
                        label="Total"
                        required
                    ></v-text-field>


                    <v-textarea
                        disabled
                        filled
                        label="ข้อความทั้งหมด"
                        auto-grow
                        v-model="texts"
                    ></v-textarea>
                    <v-card-actions>
                      <v-btn block
                             color="success"
                             class="mr-4"
                      >
                        ยืนยัน
                      </v-btn>
                    </v-card-actions>
                  </v-card-text>
                </v-form>
              </v-card>
            </v-col>
          </v-row>
        </v-container>
      </v-app>
    </div>
  </div>
  <script>
      new Vue({
          el: '#app',
          vuetify: new Vuetify(),
          data() {
              return {
                  spinner: true,
                  file: '',
                  files: null,
                  texts: '',
                  form: {},
              }
          },
          watch: {
              texts: 'showData',

          },
          methods: {
              showData() { // condition
                  if (this.texts) {
                      this.spinner = true
                  }
              },
              postData() {
                  if (this.files) {
                      this.spinner = false
                      let formData = new FormData();
                      formData.append('file', this.files)
                      axios.post('/index', formData,
                          {
                              headers: {
                                  'Content-Type': 'multipart/form-data'
                              }
                          })
                          .then((res) => {
                              let texts = res.data.texts;
                              let form = res.data.form;
                              this.texts = texts
                              this.form = form
                              console.log(form)
                              console.log(texts)
                          })
                          .catch((err) => {
                              console.error(err)
                          })
                  }
              }
          },
          delimiters: ["[[", "]]"]
      })
  </script>



{% endblock %}









