const notificationStore = {
    data : {
        showNotification : false,
        notificationTimeout : 2000,
        notificationText : "",
        isError : false,
    },
    methods : {
        showNotification(obj) {
            notificationStore.data.notificationText = obj.text;
            notificationStore.data.isError = obj.isError;
            notificationStore.data.showNotification = true;
        },
        closeNotification() {
            this.notificationTimeout = 2000;
            this.notificationText = "";
            this.isError = false;
            this.showNotification = false;
        }
    },
};

export default notificationStore;
