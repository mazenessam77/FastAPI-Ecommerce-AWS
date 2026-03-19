from sqlalchemy.orm import Session, joinedload
from fastapi import HTTPException, status
from app.models.models import Order, OrderItem, Product
from app.schemas.orders import CheckoutRequest
from app.core.security import get_current_user
from app.utils.responses import ResponseHandler


class OrderService:

    @staticmethod
    def checkout(token, db: Session, request: CheckoutRequest):
        user_id = get_current_user(token)

        if not request.items:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cart is empty",
            )

        order_items = []
        total_amount = 0.0

        for item in request.items:
            product = db.query(Product).filter(
                Product.id == item.product_id,
                Product.is_published == True,
            ).first()
            if not product:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Product {item.product_id} not found",
                )
            if product.stock < item.quantity:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Insufficient stock for '{product.title}' (available: {product.stock})",
                )

            unit_price = product.price * (1 - product.discount_percentage / 100)
            subtotal = unit_price * item.quantity
            total_amount += subtotal

            order_items.append(
                OrderItem(
                    product_id=item.product_id,
                    quantity=item.quantity,
                    unit_price=unit_price,
                    subtotal=subtotal,
                )
            )
            # Deduct stock
            product.stock -= item.quantity

        order = Order(
            user_id=user_id,
            total_amount=total_amount,
            order_items=order_items,
        )
        db.add(order)
        db.commit()
        db.refresh(order)

        return ResponseHandler.create_success("Order", order.id, order)

    @staticmethod
    def get_orders(token, db: Session, page: int, limit: int):
        user_id = get_current_user(token)
        orders = (
            db.query(Order)
            .options(joinedload(Order.order_items))
            .filter(Order.user_id == user_id)
            .order_by(Order.created_at.desc())
            .offset((page - 1) * limit)
            .limit(limit)
            .all()
        )
        return ResponseHandler.success(f"Page {page} with {limit} orders", orders)

    @staticmethod
    def get_order(token, db: Session, order_id: int):
        user_id = get_current_user(token)
        order = (
            db.query(Order)
            .options(joinedload(Order.order_items))
            .filter(Order.id == order_id, Order.user_id == user_id)
            .first()
        )
        if not order:
            ResponseHandler.not_found_error("Order", order_id)
        return ResponseHandler.get_single_success("order", order_id, order)
