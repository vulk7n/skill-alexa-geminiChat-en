# Alexa GeminiChat
### Alexa Skill Model for Integrating Google Gemini with Alexa Devices

**Visit the [Scintilla Hub](http://googleusercontent.com/youtube/0) channel on YouTube**

## Requirements
* With a Google account, generate an API authentication key on the [Google AI Developer](https://ai.google.dev/) site. Copy and save the key, as it will only be visible at the moment of creation.
* Create an [Amazon](https://www.amazon.com/ap/signin?openid.pape.preferred_auth_policies=Singlefactor&clientContext=132-2293245-7926858&openid.pape.max_auth_age=7200000&openid.return_to=https%3A%2F%2Fdeveloper.amazon.com%2Falexa%2Fconsole%2Fask&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.assoc_handle=amzn_dante_us&openid.mode=checkid_setup&marketPlaceId=ATVPDKIKX0DER&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&) account and log in to the _Alexa Developer Console_.

## Creating the Alexa Skill
Create an Alexa-hosted (Python) Skill in the Alexa console: (_Create Skill_)

1.  **Name your Skill:** Choose a name you prefer (e.g., GeminiGPT).
2.  **Choose a primary locale:** Portuguese (BR)
3.  Click **Next**. In the experience type section, select: **Other > Custom > Alexa-hosted (Python)**.
4.  **Hosting region:** You can leave the default, **US East (N. Virginia)**.
5.  Under **Templates**: Click on **Import Skill**.
6.  Enter the repository address: `https://github.com/Machally/skill-alexa-geminiChat-en.git` and confirm.

## Configuring the Skill
After the import is complete, go to **Invocations > Skill Invocation Name**:
1.  Edit the **Skill Invocation Name**. This will be the command to invoke your skill. Pay attention to the word requirements and restrictions.
2.  Click **Save**.
3.  Build the Skill by clicking on **Build Skill**. Once finished, go to the **Code** tab.
4.  Create a file inside the `lambda` folder named `.env` and add the following line, including the API key you generated:
    ```shell
    GOOGLE_API_KEY=YourGoogleAIAPIKey
    ```
5.  Click **Save** and then **Deploy**.

## Testing the Skill
After the deployment is finished, go to the **Test** tab:
1.  Under _Skill testing is enabled in_, change the setting from **Off** to **Development**.
2.  To use voice commands, accept the website's request to use your microphone. To speak, click and hold the mic icon, and release it to send.
3.  Use the configured activation command to start the Skill, and you're ready to interact with Gemini through Alexa!

The Skill will now be available on all Alexa devices linked to your account.
