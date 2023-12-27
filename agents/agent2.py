from uagents import Agent, Context, Model

class Message(Model):
    message: str

RECIPIENT_ADDRESS = "agent1qv2l7qzcd2g2rcv2p93tqflrcaq5dk7c2xc7fcnfq3s37zgkhxjmq5mfyvz"  # Replace with the actual address of Agent1

agent2 = Agent(
    name="agent2",
    port=8000,
    seed="alice secret phrase",
    endpoint=["http://127.0.0.1:8000/submit"],
)

@agent2.on_interval(period=2.0)
async def send_message(ctx: Context):
    # await ctx.send(RECIPIENT_ADDRESS, Message(message="Hello there bob."))
    ctx.logger.info("{}",ctx.address)

@agent2.on_message(model=Message)
async def message_handler(ctx: Context, sender: str, msg: Message):
    if "Score is" in msg.message:
        score = float(msg.message.split()[-1])
        if score < 50:
            # Add code to send email here
            ctx.logger.info("Sending email due to low score")
        else:
            ctx.logger.info("No need to send email")

if __name__ == "__main__":
    agent2.run()
