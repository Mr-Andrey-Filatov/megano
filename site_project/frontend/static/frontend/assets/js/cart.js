var mix = {
    methods: {
        getCartItems() {
            this.getData("/api/cart")
              .then(data => {
                this.cartProducts = data.items
              })
        },
        submitBasket () {
            this.postData('/api/orders/', {status: 'created'})
                .then(data => {
                    this.basket = {}
                    location.assign(`/order/${data.id}`)
                }).catch(() => {
                    console.warn('Ошибка при создании заказа')
                })
        }
    },
    mounted() {
        // this.getCartItems();
    },
    data() {
        return {
            cartProducts: [],
        }
    }
}