var updatebtns = document.getElementsByClassName('update-cart')

for(var i=0 ;i < updatebtns.length; i++){
    updatebtns[i].addEventListener('click', function(){
        var productid = this.dataset.product
        var action = this.dataset.action
        console.log('productid:',productid,'action:',action)
        console.log('USER:',user)
        if(user === 'AnonymousUser'){
            addCookieItem(productid,action)
        }else{
            updateUserOrder(productid,action)
        }
        location.reload()
    })
}

function updateUserOrder(productid,action){
    console.log('User is logged in, sending data..')
    var url = '/update_item/'

    fetch(url, {
        method: 'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken':csrftoken,
        },
        body:JSON.stringify({'productid':productid, 'action':action})
    })

    .then((response) =>{
        return response.json()
    })
    .then((data) =>{
        console.log('data',data)
        location.reload()
    })

}

function addCookieItem(productid, action){
	console.log('User is not authenticated')

	if (action == 'add'){
		if (cart[productid] == undefined){
		cart[productid] = {'quantity':1}

		}else{
			cart[productid]['quantity'] += 1
		}
	}

	if (action == 'remove'){
		cart[productid]['quantity'] -= 1

		if (cart[productid]['quantity'] <= 0){
			console.log('Item should be deleted')
			delete cart[productid];
		}
	}
	console.log('CART:', cart)
	document.cookie ='cart=' + JSON.stringify(cart) + ";domain=;path=/"

	location.reload()
}