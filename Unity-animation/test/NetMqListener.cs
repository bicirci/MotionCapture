using System.Collections.Concurrent;
using System.Threading;
using NetMQ;
using UnityEngine;
using NetMQ.Sockets;

// modification of PUB/SUB model at: https://github.com/valkjsaaa/Unity-ZeroMQ-Example
public class NetMqListener
{
    private int _LISTEN_PORT = 5555;
    private readonly Thread _listenerWorker;
    private bool _listenerCancelled; // controls thread termination
    public delegate void MessageDelegate(string message, string bodyPart); // delegate: holds ref to method
    private readonly MessageDelegate _messageDelegate; // ref to external logic in ClientObject (to process msg)
    private readonly ConcurrentQueue<string> _messageQueue = new ConcurrentQueue<string>();
    private string _bodyPart; // topic to subscribe to

    private void ListenerWork()
    {
        AsyncIO.ForceDotNet.Force();
        using (var subSocket = new SubscriberSocket())
        {
            subSocket.Options.ReceiveHighWatermark = 1000;
            subSocket.Connect("tcp://localhost:" + _LISTEN_PORT.ToString());

            // define body part to monitor
            subSocket.Subscribe(_bodyPart);

            // this thread just reads messages from ZeroMQ queues into its own internal queue
            while (!_listenerCancelled)
            {
                string frameString;
                if (!subSocket.TryReceiveFrameString(out frameString)) continue; // get topic of (atomic) msg
                frameString = subSocket.ReceiveFrameString(); // ignore topic, get contents of msg
                _messageQueue.Enqueue(frameString);
            }
            subSocket.Close();
        }
        NetMQConfig.Cleanup();
    }

    public void Update() // let ClientObject handle the message use case, logic
    {
        while (!_messageQueue.IsEmpty)
        {
            string message;
            if (_messageQueue.TryDequeue(out message))
            {
                _messageDelegate(message, _bodyPart);
            }
            else
            {
                break;
            }
        }
    }

    public NetMqListener(MessageDelegate messageDelegate, string bodyPart) // constructor
    {
        _messageDelegate = messageDelegate;
        _bodyPart = bodyPart;
        _listenerWorker = new Thread(ListenerWork);
    }

    public void Start() // thread logic - map to life cycle of ClientObject
    {
        _listenerCancelled = false;
        _listenerWorker.Start();
    }

    public void Stop() // thread logic - map to life cycle of ClientObject
    {
        _listenerCancelled = true;
        _listenerWorker.Join();
    }
}
