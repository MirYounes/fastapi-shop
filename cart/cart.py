import settings
import redis


redis = redis.Redis(host='redis', port='6379')


class Cart:
    PREFIX = settings.CART_PREFIX
    EXPIRE = settings.CART_EXPIRE

    @classmethod
    def add_to_cart(cls, **kwargs):
        user_id = kwargs.get('user_id')
        product_id = kwargs.get('product_id')
        cart_name = f'{cls.PREFIX}_{user_id}_{product_id}'

        if redis.exists(cart_name):
            redis.hincrby(cart_name, 'quantity', kwargs['quantity'])

        else:
            [redis.hset(cart_name, field, value)
             for field, value in kwargs.items()]
            redis.expire(cart_name, cls.EXPIRE)

        return 'cart added/changed'

    @classmethod
    def get_cart(cls, user_id):
        cart = []
        for user_carts in redis.scan_iter(f'{cls.PREFIX}_{user_id}_*'):
            data = {key.decode('utf-8'): value.decode('utf-8')
                    for key, value in redis.hgetall(user_carts).items()}
            cart.append(data)
        
        return cart
    
    @classmethod
    def delete_product(cls, user_id, product_id):
        cart_name = f'{cls.PREFIX}_{user_id}_{product_id}'
        return redis.delete(cart_name)        
    
    @classmethod
    def delete_cart(cls, user_id):
        for user_carts in redis.scan_iter(f'{cls.PREFIX}_{user_id}_*'):
            redis.delete(user_carts)  
