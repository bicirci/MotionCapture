using System.Collections.Concurrent;
using System.Threading;
using NetMQ;
using UnityEngine;
using NetMQ.Sockets;
// (no import statement required if in same directory), i.e. for NetMqListener.cs

// modification of PUB/SUB model at: https://github.com/valkjsaaa/Unity-ZeroMQ-Example
// NOTE: if you are duplicating this file, make sure to change the filename and the name of the class
// change the handler logic and body part specified as well


public class ClientBodyPart : MonoBehaviour
{
    private string _LEFT_HAND = "Left Hand";
    private string _LEFT_FOREARM = "Left Forearm";
    private string _LEFT_UPPER_ARM = "Left Upper Arm";
    private string _RIGHT_HAND = "Right Hand";
    private string _RIGHT_FOREARM = "Right Forearm";
    private string _RIGHT_UPPER_ARM = "Right Upper Arm";

    private NetMqListener _netMqBodyPart;

    // NOTE: modify this handler for our COMP6733 use case
    private void HandleBodyPartMessage(string message, string bodyPart)
    {
        //Debug.Log("ClientObject: BodyPartMessage: " + bodyPart + ": " + message);
        var splittedStrings = message.Split(',');
        if (splittedStrings.Length != 5) return;
        var time = float.Parse(splittedStrings[0]);
        var q0 = float.Parse(splittedStrings[1]);
        var q1 = float.Parse(splittedStrings[2]);
        var q2 = float.Parse(splittedStrings[3]);
        var q3 = float.Parse(splittedStrings[4]);
        Debug.Log(string.Format("time={0}, q0={1}, q1={2}, q2={3}, q3={4}", time, q0, q1, q2, q3));
        
        //transform.position = new Vector3(x, y, z);
    }
    private void HandleLogMessage(string message, string topic)
    {
        Debug.Log("ClientObject: LogMessage: " + topic + ": " + message);
    }

    private void Start()
    {
        // NOTE: modify the body part argument for our COMP6733 use case
        _netMqBodyPart = new NetMqListener(HandleBodyPartMessage, _LEFT_HAND);
        _netMqBodyPart.Start();
    }

    private void Update()
    {
        _netMqBodyPart.Update();
    }

    private void OnDestroy()
    {
        _netMqBodyPart.Stop();
    }
}
