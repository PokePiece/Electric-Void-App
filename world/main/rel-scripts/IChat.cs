using UnityEngine;
using UnityEngine.Networking;
using System.Collections;
using TMPro; // For TextMeshPro UI text

public class AIChat : MonoBehaviour
{
    public TMP_InputField inputField; // The input field in your game UI
    public TMP_Text outputText; // Where the AI's reply will be shown
    private string apiUrl = "http://localhost:8005/chat"; // Public server URL

    public void SendMessageToAI()
    {
        string userMessage = inputField.text;
        if (!string.IsNullOrEmpty(userMessage))
        {
            StartCoroutine(SendMessageCoroutine(userMessage));
        }
    }

    IEnumerator SendMessageCoroutine(string message)
    {
        string jsonData = JsonUtility.ToJson(new ChatRequest(message));

        UnityWebRequest request = new UnityWebRequest(apiUrl, "POST");
        byte[] bodyRaw = System.Text.Encoding.UTF8.GetBytes(jsonData);
        request.uploadHandler = new UploadHandlerRaw(bodyRaw);
        request.downloadHandler = new DownloadHandlerBuffer();
        request.SetRequestHeader("Content-Type", "application/json");

        yield return request.SendWebRequest();

        if (request.result != UnityWebRequest.Result.Success)
        {
            outputText.text = "Error: " + request.error;
        }
        else
        {
            ChatResponse response = JsonUtility.FromJson<ChatResponse>(request.downloadHandler.text);
            outputText.text = response.reply;
        }
    }

    [System.Serializable]
    public class ChatRequest
    {
        public string message;
        public ChatRequest(string msg) { message = msg; }
    }

    [System.Serializable]
    public class ChatResponse
    {
        public string reply;
    }
}
