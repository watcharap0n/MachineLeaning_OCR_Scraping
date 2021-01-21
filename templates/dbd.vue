{% extends "layout.html" %}
{% block content %}
    <br>
    <br>
    <br>
    <br>
    <div id="app">
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
                                    v-model="valid"
                                    lazy-validation
                            >
                                <v-card-text>
                                    <v-text-field
                                            dense
                                            outlined
                                            clearable
                                            label="หมายเลขผู้เสียภาษี"
                                            required
                                            v-model="push_tax"
                                    >
                                        <v-btn
                                                :loading="!spinButton"
                                                x-small
                                                slot="append"
                                                color="green"
                                                @click="creatTable({'push_tax': push_tax})"
                                        >
                                            <v-icon
                                                    color="white"
                                            >
                                                mdi-account-search-outline
                                            </v-icon>
                                        </v-btn>
                                    </v-text-field>

                                    <v-text-field
                                            dense
                                            outlined
                                            clearable
                                            label="ชื่อนิติบุคคล"
                                            required
                                            v-model="formElement.fname"
                                    ></v-text-field>
                                    <v-text-field
                                            dense
                                            outlined
                                            clearable
                                            label="ประเภทนิติบุคคล"
                                            required
                                            v-model="formElement.type_person"
                                    ></v-text-field>

                                    <v-text-field
                                            dense
                                            outlined
                                            clearable
                                            label="สถานะ"
                                            required
                                            v-model="formElement.status"
                                    ></v-text-field>

                                    <v-text-field
                                            dense
                                            outlined
                                            clearable
                                            label="รหัสประเภทธรุกิจ"
                                            required
                                            v-model="formElement.bus_id"
                                    ></v-text-field>

                                    <v-text-field
                                            dense
                                            outlined
                                            clearable
                                            label="ชื่อประเภทธรุกิจ"
                                            required
                                            v-model="formElement.bus_name"
                                    ></v-text-field>

                                    <v-text-field
                                            dense
                                            outlined
                                            clearable
                                            label="จังหวัด"
                                            required
                                            v-model="formElement.city"
                                    ></v-text-field>

                                    <v-text-field
                                            dense
                                            outlined
                                            clearable
                                            label="ทุนจดทะเบียน(บาท)"
                                            required
                                            v-model="formElement.authorized"
                                    ></v-text-field>

                                    <v-text-field
                                            dense
                                            outlined
                                            clearable
                                            label="รายได้รวม(บาท)"
                                            required
                                            v-model="formElement.credit"
                                    ></v-text-field>

                                    <v-text-field
                                            dense
                                            outlined
                                            clearable
                                            label="กำไร(ขาดทุน)สุทธิ(บาท)"
                                            required
                                            v-model="formElement.profit"
                                    ></v-text-field>

                                    <v-text-field
                                            dense
                                            outlined
                                            clearable
                                            label="สินทรัพย์รวม(บาท)"
                                            required
                                            v-model="formElement.keep_profit"
                                    ></v-text-field>


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



    <script>

        new Vue({
            el: '#app',
            vuetify: new Vuetify(),
            data() {
                return {
                    headers: [
                        {text: 'index', value: 'index'},
                        {text: 'tax_id', value: 'tax_id'},
                        {text: 'fname', value: 'fname'},
                        {text: 'type_person', value: 'type_person'},
                        {text: 'status', value: 'status'},
                    ],
                    formElement: {
                        fname: '',
                        type_person: '',
                        status: '',
                        bus_id: '',
                        bus_name: '',
                        city: '',
                        authorized: '',
                        credit: '',
                        profit: '',
                        keep_profit: '',
                        prices: ''
                    },
                    valid: false,
                    dialog: true,
                    push_tax: '',
                    spinButton: true,
                    hiddenTable: false,
                    dbd: {},
                }
            },
            watch: {
                dbd: 'showData'
            },
            methods: {
                showData() {
                    if (this.dbd) {
                        this.spinButton = true
                    }
                },
                creatTable(data) {
                    if (this.push_tax) {
                        this.dialog = false;
                        this.spinButton = false;
                        const path = '/data_dbd';
                        axios.post(path, data)
                            .then((res) => {
                                let dbd = res.data.dbd;
                                this.dbd = dbd
                                dbd.forEach(data => {
                                    this.formElement.fname = data.fname;
                                    this.formElement.type_person = data.type_person;
                                    this.formElement.status = data.status;
                                    this.formElement.bus_id = data.bus_id;
                                    this.formElement.bus_name = data.bus_name;
                                    this.formElement.city = data.city;
                                    this.formElement.authorized = data.authorized;
                                    this.formElement.credit = data.credit;
                                    this.formElement.profit = data.profit;
                                    this.formElement.keep_profit = data.keep_profit;
                                    this.formElement.prices = data.prices;
                                })
                                this.hiddenTable = true;
                                console.log(this.dbd);
                            })
                            .catch((err) => {
                                console.error(err);
                            })
                    }
                },
            },
            delimiters: ["[[", "]]"]
        });

    </script>

{% endblock %}
