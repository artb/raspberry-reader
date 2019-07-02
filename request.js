const qrCode = process.argv[2];
const establishmentId = '5d12146d8d763e002631c884';
const axios = require('axios');
// ec2-54-209-181-18.compute-1.amazonaws.com
console.log('qr code', qrCode);
const init = async () => {
        try {
                const response = await axios.post(`http://192.168.43.115:80/transactions/transaction/${qrCode}/${establishmentId}`,
                        {
                                'type': 'checkout',
                        },
                        {
                                params: {
                                        providerId: qrCode,
                                        recipientId: establishmentId,
                                },
                                'Content-Type': 'application/json'
                        });
                console.log(response.data, response.status);
                process.exit(0);
        } catch (e) {
                console.log(e.response.data);
                process.exit(-1);
        }
}

init();


