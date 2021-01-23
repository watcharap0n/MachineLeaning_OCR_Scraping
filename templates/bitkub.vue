{% extends "layout.html" %}
{% block content %}
  <br>
  <br>
  <br>
  <br>
  <div class="text-center">
    RPA WebScraping
  </div>
  <div id="app">
    <v-app id="inspire">
      <v-container>
        <div class="text-center">
          <v-btn
              color="primary"
              dark
              @click="creatTable"
              :loading="spinButton"
          >
            LoadData
          </v-btn>
        </div>
        <v-data-table
            :loading="spinButton"
            :headers="headers"
            :items="bitkub"
            :items-per-page="10"
            class="elevation-1"
        ></v-data-table>
      </v-container>
    </v-app>
  </div>

  <script>

      new Vue({
          el: '#app',
          vuetify: new Vuetify(),
          data() {
              return {
                  headers: [
                      {text: 'สกุลเงิน', value: 'coin'},
                      {text: 'ราคาล่าสุด', value: 'price_last'},
                      {text: 'ซื้อขายวันนี้', value: 'buy_sell'},
                      {text: 'สูงสุดวันนี้', value: 'peak'},
                      {text: 'ต่ำสุดวันนี้', value: 'lower'},

                  ],
                  spinButton: true,
                  bitkub: [],
                  hiddenTable: false,
              }
          },
          created() {
              this.creatTable();
          },
          methods: {
              creatTable() {
                  const path = '/data_bitkub';
                  axios.get(path)
                      .then((res) => {
                          this.bitkub = res.data.bitkub;
                          this.spinButton = false
                          this.hiddenTable = true
                          console.log(this.bitkub)
                      })
                      .catch((err) => {
                          console.error(err)
                      })
              },
          },
          delimiters: ["[[", "]]"]
      });

  </script>

{% endblock %}
