{% extends "layout.html" %}
{% block content %}

    <br>
    <br>
    <br>
    <br>
    <div id="app">
        <div id="app">
            <v-app id="inspire">
                <v-container>
                    <v-dialog
                            v-model="dialog"
                            persistent
                            max-width="500"
                    >
                        <template v-slot:activator="{ on, attrs }">
                            <v-btn
                                    color="primary"
                                    dark
                                    v-bind="attrs"
                                    v-on="on"
                            >
                                Open Dialog
                            </v-btn>
                        </template>
                        <v-card>
                            <v-card-title class="headline">
                                ค้นหาข้อมูลตลาดส่งออกสำคัญ ตามโครงสร้างสินค้ากระทรวงพาณิชย์
                            </v-card-title>
                            <v-card-text>
                                <v-row>
                                    <v-col cols="6">
                                        <v-text-field
                                                v-model="formElement.keyword"
                                                label="คำค้นหา">
                                        </v-text-field>
                                    </v-col>
                                    <v-col cols="6">
                                        <v-text-field label="ปี"
                                                      v-model="formElement.revision"
                                                      type="number">

                                        </v-text-field>
                                    </v-col>
                                </v-row>

                                <v-row>
                                    <v-col cols="6">
                                        <v-select
                                                v-model="formElement.imex_type"
                                                :items="items"
                                                label="นำเข้าหรือส่งออก"
                                        ></v-select>
                                    </v-col>
                                    <v-col cols="6">
                                        <v-select
                                                v-model="formElement.order_by"
                                                :items="orders"
                                                label="รูปแบบการเรียงลำดับข้อมูลส่งออก">
                                        </v-select>
                                    </v-col>
                                </v-row>

                            </v-card-text>
                            <v-card-actions>
                                <v-spacer></v-spacer>
                                <v-btn
                                        color="green darken-1"
                                        text
                                        @click="dialog = false"
                                >
                                    Disagree
                                </v-btn>
                                <v-btn
                                        color="green darken-1"
                                        text
                                        @click="saveData"
                                >
                                    Agree
                                </v-btn>
                            </v-card-actions>
                        </v-card>
                    </v-dialog>
                    <v-data-table
                            :hidden="!hiddenTable"
                            :headers="headers"
                            :items="ministries"
                            :items-per-page="10"
                            class="elevation-1"
                    ></v-data-table>
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
                    headers: [
                        {text: 'สกุลเงิน', value: 'com_code'},
                        {text: 'อธิบายไทย', value: 'com_description_th'},
                        {text: 'อื่นๆ', value: 'hs_description_th'},
                    ],
                    formElement: {
                        keyword: '',
                        revision: '',
                        imex_type: '',
                        order_by: ''
                    },
                    orders: ['hs_code', 'com_code'],
                    items: ['import', 'export'],
                    ministries: [],
                    dialog: true,
                    hiddenTable: false,
                }
            },
            methods: {
                saveData() {
                    this.postData(this.formElement);
                    this.dialog = false;
                },
                postData(data) {
                    const path = '/data_ministry'
                    axios.post(path, data)
                        .then((res) => {
                            let data = this.ministries = res.data.ministry;
                            this.hiddenTable = true;
                            console.log(data)
                        })
                        .catch((err) => {
                            console.error(err)
                        })
                }
            },
            delimiters: ["[[", "]]"]
        })
    </script>

{% endblock %}