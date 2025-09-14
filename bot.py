import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
import json
import os
from datetime import datetime

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Bot configuration
BOT_TOKEN = "7895866430:AAGK_aniRli6UmhRek09go7VoCd3T6gaXVE"
ADMIN_ID = 6317648827

# File to store orders
ORDERS_FILE = "orders.json"

def load_orders():
    """Load orders from file"""
    if os.path.exists(ORDERS_FILE):
        try:
            with open(ORDERS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_orders(orders):
    """Save orders to file"""
    with open(ORDERS_FILE, 'w', encoding='utf-8') as f:
        json.dump(orders, f, ensure_ascii=False, indent=2)

# Load existing orders
orders = load_orders()
order_counter = max([int(k) for k in orders.keys()] + [0])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a welcome message when /start command is issued"""
    welcome_text = """
🎮 **Free Fire Diamond Shop এ স্বাগতম!** 🎮

আপনার গেমিং অভিজ্ঞতাকে আরও উন্নত করতে আমরা এখানে আছি!

✨ **আমাদের সেবাসমূহ:**
• দ্রুত ও নির্ভরযোগ্য ডায়মন্ড টপআপ
• সাশ্রয়ী মূল্যে প্রিমিয়াম সেবা
• ২৪/৭ কাস্টমার সাপোর্ট

🚀 **শুরু করতে /topup কমান্ড ব্যবহার করুন**

আরও কমান্ডের জন্য /commands টাইপ করুন।

FIRE ARENA! 🔥
    """
    await update.message.reply_text(welcome_text, parse_mode='Markdown')

async def commands(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show available commands"""
    commands_text = """
📋 **বট কমান্ড তালিকা:**

🔹 **/start** - স্বাগতম বার্তা
🔹 **/topup** - ডায়মন্ড প্যাকেজ দেখুন
🔹 **/confirm** - অর্ডার কনফার্ম করুন
   📝 Format: `/confirm uid ingamename diamond method txid`
🔹 **/like** - ১০০ লাইক অর্ডার করুন
🔹 **/number** - পেমেন্ট নাম্বার দেখুন
🔹 **/help** - সাহায্য পেতে যোগাযোগ করুন
🔹 **/commands** - এই তালিকা

💡 **টিপস:** কোন সমস্যা হলে /help ব্যবহার করুন!
    """
    await update.message.reply_text(commands_text, parse_mode='Markdown')

async def topup(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show topup packages"""
    topup_text = """
💎 **Free Fire Diamond Packages** 💎

🔸 **20 💎** - **22 টাকা**
🔸 **50 💎** - **36 টাকা**
🔸 **115 💎** - **77 টাকা**
🔸 **240 💎** - **153 টাকা**
🔸 **610 💎** - **385 টাকা**
🔸 **1240 💎** - **770 টাকা**
🔸 **2530 💎** - **1530 টাকা**

📅 **সাবস্ক্রিপশন প্যাকেজ:**
🔸 **Weekly** - **153 টাকা**
🔸 **Monthly** - **755 টাকা**

❤️ **বোনাস সার্ভিস:**
🔸 **100 Like** - **10 টাকা**

📞 **অর্ডার করতে:** `/confirm` কমান্ড ব্যবহার করুন
💳 **পেমেন্ট নাম্বার:** `/number` কমান্ড ব্যবহার করুন

⚡ **দ্রুত ডেলিভারি গ্যারান্টি!**
    """
    await update.message.reply_text(topup_text, parse_mode='Markdown')

async def confirm_order(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Process order confirmation"""
    global order_counter, orders
    
    try:
        # Parse command arguments
        args = context.args
        if len(args) != 5:
            await update.message.reply_text(
                "❌ **ভুল ফরমেট!**\n\n"
                "📝 **সঠিক ফরমেট:**\n"
                "`/confirm uid ingamename diamond method txid`\n\n"
                "**উদাহরণ:**\n"
                "`/confirm 123456789 PlayerName 610💎 BKash TXN123456`",
                parse_mode='Markdown'
            )
            return
        
        uid, ingame_name, diamond_amount, method, txid = args
        
        # Generate order ID
        order_counter += 1
        order_id = str(order_counter)
        
        # Store order
        orders[order_id] = {
            'user_id': update.effective_user.id,
            'username': update.effective_user.username or 'N/A',
            'uid': uid,
            'ingame_name': ingame_name,
            'diamond_amount': diamond_amount,
            'method': method,
            'txid': txid,
            'timestamp': datetime.now().isoformat(),
            'status': 'pending'
        }
        
        # Save orders
        save_orders(orders)
        
        # Send confirmation to user
        user_message = f"""
✅ **অর্ডার সফলভাবে জমা দেওয়া হয়েছে!**

🆔 **অর্ডার নাম্বার:** #{order_id}
👤 **UID:** `{uid}`
🎮 **গেম নেম:** {ingame_name}
💎 **ডায়মন্ড:** {diamond_amount}
💳 **পেমেন্ট মেথড:** {method}
🧾 **TXN ID:** `{txid}`

⏳ **আপনার অর্ডার প্রসেসিং এ আছে...**

ধন্যবাদ! 🙏
        """
        
        await update.message.reply_text(user_message, parse_mode='Markdown')
        
        # Send order details to admin
        admin_message = f"""
🔔 **নতুন অর্ডার - #{order_id}**

👤 **কাস্টমার তথ্য:**
- **User ID:** {update.effective_user.id}
- **Username:** @{update.effective_user.username or 'N/A'}
- **নাম:** {update.effective_user.full_name}

🎮 **অর্ডার বিবরণ:**
- **FF UID:** `{uid}`
- **গেম নেম:** {ingame_name}
- **ডায়মন্ড:** {diamond_amount}
- **পেমেন্ট:** {method}
- **TXN ID:** `{txid}`

⏰ **অর্ডার সময়:** {datetime.now().strftime('%d/%m/%Y %I:%M %p')}

**অ্যাকশন:**
• `/accept #{order_id} completed✅` - গ্রহণ করুন
• `/cancel #{order_id} reason:কারণ` - বাতিল করুন
        """
        
        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=admin_message,
            parse_mode='Markdown'
        )
        
    except Exception as e:
        logger.error(f"Error in confirm_order: {e}")
        await update.message.reply_text(
            "❌ **অর্ডার প্রসেসিং এ সমস্যা হয়েছে!**\n\n"
            "দয়া করে আবার চেষ্টা করুন বা /help এ যোগাযোগ করুন।"
        )

async def like_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle like command"""
    like_message = """
❤️ **100 লাইক অর্ডার করেছেন!**

📋 **বিবরণ:**
• **সার্ভিস:** 100 Like
• **মূল্য:** 10 টাকা
• **ডেলিভারি:** প্রতিদিন ১০০টি

⚠️ **গুরুত্বপূর্ণ নোট:**
- প্রতিদিন ১০০টি লাইক যাবে
- কোন দিন কম গেলে পরের দিন পূরণ করে দেওয়া হবে
- মোট ১০০টি লাইক গ্যারান্টি!

💳 **পেমেন্ট:** `/number` কমান্ড দিয়ে নাম্বার দেখুন
📞 **অর্ডার কনফার্ম:** `/confirm` ব্যবহার করুন

ধন্যবাদ! 🙏
    """
    await update.message.reply_text(like_message, parse_mode='Markdown')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show help information"""
    help_text = """
🆘 **সাহায্য প্রয়োজন?**

আমাদের সাপোর্ট টিমের সাথে যোগাযোগ করুন:

👨‍💼 **Admin Contact:**
📱 **Telegram:** @toushif56

💬 **সাহায্যের জন্য মেসেজ করুন!**

🕒 **সাপোর্ট সময়:** 24/7 Available
⚡ **দ্রুত রেসপন্স গ্যারান্টি**

আমরা আপনার সেবায় নিয়োজিত! 🤝
    """
    await update.message.reply_text(help_text, parse_mode='Markdown')

async def number_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show payment numbers"""
    
    # Create inline keyboard with copyable numbers
    keyboard = [
        [InlineKeyboardButton("📱 BKash: 01799061749", callback_data="copy_bkash")],
        [InlineKeyboardButton("💳 Nagad: 01799061749", callback_data="copy_nagad")],
        [InlineKeyboardButton("🟡 Binance: 772652360", callback_data="copy_binance")],
        [InlineKeyboardButton("🔶 Bybit: 506222609", callback_data="copy_bybit")]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    numbers_text = """
💳 **পেমেন্ট অপশনসমূহ:**

📱 **BKash:** `01799061749`
💳 **Nagad:** `01799061749`
🟡 **Binance ID:** `772652360`
🔶 **Bybit ID:** `506222609`

💰 **Crypto Rate:**
• **Binance/Bybit:** ১২০ টাকা = ১ ডলার

⚠️ **গুরুত্বপূর্ণ:**
- পেমেন্ট করার পর TXN ID সেভ করুন
- সঠিক পরিমাণ পাঠান
- `/confirm` কমান্ড দিয়ে অর্ডার কনফার্ম করুন

নাম্বার কপি করতে উপরের বাটনে ক্লিক করুন! 👆
    """
    
    await update.message.reply_text(numbers_text, parse_mode='Markdown', reply_markup=reply_markup)

async def accept_order(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Accept order (Admin only)"""
    if update.effective_user.id != ADMIN_ID:
        return
    
    try:
        message_text = update.message.text
        # Parse: /accept #1 completed✅
        parts = message_text.split(' ', 2)
        if len(parts) < 2:
            return
            
        order_id = parts[1].replace('#', '')
        status_msg = parts[2] if len(parts) > 2 else "completed✅"
        
        if order_id in orders:
            order = orders[order_id]
            orders[order_id]['status'] = 'completed'
            save_orders(orders)
            
            # Send completion message to customer
            completion_msg = f"""
✅ **অর্ডার সম্পন্ন হয়েছে!**

🆔 **অর্ডার নাম্বার:** #{order_id}
💎 **ডায়মন্ড:** {order['diamond_amount']}
🎮 **গেম নেম:** {order['ingame_name']}

🎉 **আপনার ডায়মন্ড অ্যাকাউন্টে যোগ হয়ে গেছে!**

ধন্যবাদ আমাদের সাথে থাকার জন্য! 🙏
আবার অর্ডার করতে /topup ব্যবহার করুন।
            """
            
            await context.bot.send_message(
                chat_id=order['user_id'],
                text=completion_msg,
                parse_mode='Markdown'
            )
            
            # Confirm to admin
            await update.message.reply_text(f"✅ অর্ডার #{order_id} সম্পন্ন হয়েছে!")
            
    except Exception as e:
        logger.error(f"Error in accept_order: {e}")

async def cancel_order(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cancel order (Admin only)"""
    if update.effective_user.id != ADMIN_ID:
        return
    
    try:
        message_text = update.message.text
        # Parse: /cancel #1 reason:insufficient balance
        parts = message_text.split(' ', 2)
        if len(parts) < 3:
            return
            
        order_id = parts[1].replace('#', '')
        reason_part = parts[2]
        
        if reason_part.startswith('reason:'):
            reason = reason_part[7:]  # Remove 'reason:'
        else:
            reason = reason_part
        
        if order_id in orders:
            order = orders[order_id]
            orders[order_id]['status'] = 'cancelled'
            orders[order_id]['cancel_reason'] = reason
            save_orders(orders)
            
            # Send cancellation message to customer
            cancel_msg = f"""
❌ **অর্ডার বাতিল করা হয়েছে**

🆔 **অর্ডার নাম্বার:** #{order_id}
💎 **ডায়মন্ড:** {order['diamond_amount']}

📝 **বাতিলের কারণ:**
{reason}

💰 **আপনার পেমেন্ট রিফান্ড প্রসেস করা হবে।**

আরো জানতে: @toushif56
            """
            
            await context.bot.send_message(
                chat_id=order['user_id'],
                text=cancel_msg,
                parse_mode='Markdown'
            )
            
            # Confirm to admin
            await update.message.reply_text(f"❌ অর্ডার #{order_id} বাতিল করা হয়েছে!")
            
    except Exception as e:
        logger.error(f"Error in cancel_order: {e}")

async def handle_callback_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle inline keyboard callbacks"""
    query = update.callback_query
    await query.answer()
    
    callback_data = query.data
    
    if callback_data == "copy_bkash":
        await query.edit_message_text("📱 **BKash নাম্বার কপি করুন:**\n\n`01799061749`", parse_mode='Markdown')
    elif callback_data == "copy_nagad":
        await query.edit_message_text("💳 **Nagad নাম্বার কপি করুন:**\n\n`01799061749`", parse_mode='Markdown')
    elif callback_data == "copy_binance":
        await query.edit_message_text("🟡 **Binance ID কপি করুন:**\n\n`772652360`", parse_mode='Markdown')
    elif callback_data == "copy_bybit":
        await query.edit_message_text("🔶 **Bybit ID কপি করুন:**\n\n`506222609`", parse_mode='Markdown')

def main():
    """Start the bot"""
    # Create the Application
    application = Application.builder().token(BOT_TOKEN).build()

    # Add command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("commands", commands))
    application.add_handler(CommandHandler("topup", topup))
    application.add_handler(CommandHandler("confirm", confirm_order))
    application.add_handler(CommandHandler("like", like_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("number", number_command))
    application.add_handler(CommandHandler("accept", accept_order))
    application.add_handler(CommandHandler("cancel", cancel_order))
    
    # Add callback query handler
    from telegram.ext import CallbackQueryHandler
    application.add_handler(CallbackQueryHandler(handle_callback_query))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()