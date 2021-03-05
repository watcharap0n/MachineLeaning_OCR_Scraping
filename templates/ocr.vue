{% extends "layout.html" %}
{% block content %}

  <br><br><br>
  <div class="text-center">OCR</div>
  <div id="app">
    <v-app id="inspire">
      <v-container>
        <v-row justify="center">
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

        </v-row>

        <v-textarea
            filled
            label="ข้อความทั้งหมด"
            auto-grow
            v-model="texts"
        ></v-textarea>
      </v-container>
    </v-app>
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
                      axios.post('/ocr', formData,
                          {
                              headers: {
                                  'Content-Type': 'multipart/form-data'
                              }
                          })
                          .then((res) => {
                              let texts = res.data.texts;
                              this.texts = texts
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