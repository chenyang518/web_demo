<template>
  <div>
      <p>{{ msg }}</p>
  </div>
</template>

<script>
import axios from 'axios';

export default {
    name: 'Ping',
    data() {
        return {
            msg: [],
        };
    },
    methods: {
        getMessage() {
            const path = 'http://localhost:5000/ping';
            axios.get(path)
                .then((res) => {
                    var index = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
                    for (var i in res.data) {
                        if (res.data[i]['Headcount'] == 'Track Plan') {
                            for (var j = 0; j < index.length; j++) {
                                this.msg.push(res.data[i][index[j]]);
                            }
                        }
                            
                    }
                })
                .catch((error) => {
                    console.error(error);
                });
        },
    },
    created() {
        this.getMessage();
    },
};
</script>

<style>

</style>