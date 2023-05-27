var mix = {
    methods: {
        getOneOrder(orderId) {
            if(typeof orderId !== 'number') return
            this.getData(`/api/orders/${orderId}/`).then(data => {
                this.orderId = data.id
                this.createdAt = data.createdAt
                this.fullName = data.fullName
                this.phone = data.phone
                this.email = data.email
                this.deliveryType = data.deliveryType
                this.city = data.city
                this.address = data.address
                this.paymentType = data.paymentType
                this.status = data.status
                this.totalCost = data.totalCost
                this.products = data.products
                if (typeof data.paymentError !== 'undefined'){
                    this.paymentError = data.paymentError
                }
            })
        },
        getOrder(orderId) {
            if(typeof orderId !== 'number') return
            this.getData(`/api/orders/${orderId}/`).then(data => {
                this.order = {
                        ...data
                    }
                if (typeof data.paymentError !== 'undefined'){
                    this.paymentError = data.paymentError
                }
            })
        },
        confirmOrder() {
            if (this.order) {
                this.order.status = 'confirmed'
                this.postData('/api/orders/' + this.order.id + '/', {
                   ...this.order
                })
                    .then(() => {
                        alert('Заказ подтвержден')
                        location.replace('/payment/' + this.order.id)
                    })
                    .catch(() => {
                        console.warn('Ошибка при подтверждения заказа')
                    })
            }
        }
    },
    mounted() {
        if(location.pathname.startsWith('/order/')) {
			const orderId = location.pathname.replace('/order/', '').replace('/', '')
			this.order.id = orderId.length ? Number(orderId) : null
			this.getOrder(this.order.id);
		}
        if(location.pathname.startsWith('/order-detail/')) {
			const orderId = location.pathname.replace('/order-detail/', '').replace('/', '')
			this.orderId = orderId.length ? Number(orderId) : null
			this.getOneOrder(this.orderId);
		}
    },
    data() {
        return {
            orderId: null,
            createdAt: null,
            fullName: null,
            phone: null,
            email: null,
            deliveryType: null,
            city: null,
            address: null,
            paymentType: null,
            status: null,
            totalCost: null,
            products: [],
            paymentError: null,
        }
    },
}