from src.application.dto import Event

class Serializer:
    @staticmethod
    def serialize_event(email_message: Event):
        print(f"email_message.txt: {email_message.txt}")
        print(f"email_message.desc: {email_message.desc}")
        html = (
            f'''
            <html>
                <body>
                    <h1>{email_message.txt}</h1>
                    <h3>{email_message.desc}</h3>
                </body>
            </html>

        '''
        )
        return html