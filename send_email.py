import osascript

def escape_applescript_string(s):
    return s.replace('"', '\\"')

def create_email_draft(to_address, subject, body):
    subject = escape_applescript_string(subject)
    body = escape_applescript_string(body)
    to_address = escape_applescript_string(to_address)

    code = r'''
    tell application "Mail"
        set newMessage to make new outgoing message with properties {{subject:"{0}", content:"{1}", visible:true}}
        tell newMessage
            make new to recipient at end of to recipients with properties {{address:"{2}"}}
        end tell
        save newMessage
    end tell
    '''.format(subject, body, to_address)
    
    osa_result = osascript.run(code)
    print(osa_result)

# Testaufruf
# Uncomment the next line to test the function.
# create_email_draft("t.knapp@atis-gmbh.de", "Test", "Dies ist ein Test.")










