using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System;

// ZeroMQ
using System.Collections.Concurrent;
using System.Threading;
using NetMQ;
using NetMQ.Sockets;

public class upmove : MonoBehaviour
{
    // Start is called before the first frame update
    Animator animator;
    bool up_flag;
    bool down_flag;
    bool clap_flag;
    bool wave_flag;
    bool middle_flag;
    int clap_count;
    int wave_count;
    int up_count;
    int down_count;
    int middle_count;

    // ZeroMQ
    private string _TOPIC = "Classify";
    private NetMqListener _netMqListener;

    private void SetFlagsByMode(int mode)
    {
        // assume mode 0 means all flags are false
        up_flag     = (mode == 1) ? true : false;
        down_flag   = (mode == 2) ? true : false;
        middle_flag = (mode == 3) ? true : false;
        wave_flag   = (mode == 4) ? true : false;
        clap_flag   = (mode == 5) ? true : false;
    }

    private void HandleMessage(string message, string topicName)
    {
        Debug.Log(this.GetType().Name + ": HandleMessage: " + topicName + ": " + message);
        if (String.Compare(message, "UP") == 0)
        {
            SetFlagsByMode(1);
        } 
        else if (String.Compare(message, "DOWN") == 0)
        {
            SetFlagsByMode(2);
        } 
        else if (String.Compare(message, "MIDDLE") == 0)
        {
            SetFlagsByMode(3);
        } 
        else if (String.Compare(message, "WAVE") == 0)
        {
            SetFlagsByMode(4);
        } 
        else if (String.Compare(message, "CLAP") == 0)
        {
            SetFlagsByMode(5);
        } 
        else
        {
            SetFlagsByMode(0);
            Debug.Log(this.GetType().Name + ": HandleMessage: (no animation flags set)");
        }

        if (up_flag) up_count = 20;
        if (down_flag) down_count = 20;
        if (clap_flag) clap_count = 60;
        if (wave_flag) wave_count = 60;
        if (middle_flag) middle_count = 15;
    }


    void Start()
    {
        animator = GetComponent<Animator>();
        _netMqListener = new NetMqListener(HandleMessage, _TOPIC);
        _netMqListener.Start();
    }

    // Update is called once per frame
    void Update()
    {
        _netMqListener.Update();
        // bool moveup = Input.GetKey(KeyCode.U);
        // bool movedown = Input.GetKey(KeyCode.J);
        // bool clapin = Input.GetKey(KeyCode.I);
        // bool wave = Input.GetKey(KeyCode.W);
        // bool middle = Input.GetKey(KeyCode.M);
        
        // up_flag = (moveup) ? true : false;
        // down_flag = (movedown) ? true : false;
        // clap_flag = (clapin) ? true : false;
        // wave_flag = (wave) ? true : false;
        // middle_flag = (middle) ? true : false;

        // if (up_flag) up_count = 20;
        // if (down_flag) down_count = 20;
        // if (clap_flag) clap_count = 60;
        // if (wave_flag) wave_count = 60;
        // if (middle_flag) middle_count = 15;

        float up_percent = animator.GetFloat("upPercent");
        float clap_percent = animator.GetFloat("clapPercent");
        float wave_percent = animator.GetFloat("wavePercent");
        if (up_count > 0)
        {
            up_percent = 1;
            clap_percent = 0;
            wave_percent = 0;
            animator.SetFloat("upPercent", up_percent, 0.2f, Time.deltaTime);
            animator.SetFloat("clapPercent", clap_percent, 0.01f, Time.deltaTime);
            animator.SetFloat("wavePercent", wave_percent, 0.01f, Time.deltaTime);
            up_count--;
        }
        if (down_count > 0)
        {
            up_percent = 0;
            clap_percent = 0;
            wave_percent = 0;
            animator.SetFloat("upPercent", up_percent, 0.2f, Time.deltaTime);
            animator.SetFloat("clapPercent", clap_percent, 0.01f, Time.deltaTime);
            animator.SetFloat("wavePercent", wave_percent, 0.01f, Time.deltaTime);
            down_count--;
        }

        if (middle_count > 0)
        {
            up_percent = 0.5f;
            clap_percent = 0;
            wave_percent = 0;
            animator.SetFloat("upPercent", up_percent, 0.1f, Time.deltaTime);
            animator.SetFloat("clapPercent", clap_percent, 0.01f, Time.deltaTime);
            animator.SetFloat("wavePercent", wave_percent, 0.01f, Time.deltaTime);
            middle_count--;
        }


        if (clap_count > 0)
        {
            if(clap_count < 15)
            {
                clap_percent = 0.5f;
                animator.SetFloat("clapPercent", clap_percent, 0.1f, Time.deltaTime);
            }
            else if(clap_count < 30)
            {
                clap_percent = 1;
                animator.SetFloat("clapPercent", clap_percent, 0.1f, Time.deltaTime);
            }
            else if (clap_count < 45)
            {
                clap_percent = 0.5f;
                up_percent = 0.5f;
                wave_percent = 0;
                animator.SetFloat("upPercent", up_percent, 0.01f, Time.deltaTime);
                animator.SetFloat("wavePercent", wave_percent, 0.01f, Time.deltaTime);

                animator.SetFloat("clapPercent", clap_percent, 0.1f, Time.deltaTime);
                
            }
            else
            {
                clap_percent = 1;
                up_percent = 0.5f;
                wave_percent = 0;
                animator.SetFloat("upPercent", up_percent, 0.01f, Time.deltaTime);
                animator.SetFloat("wavePercent", wave_percent, 0.01f, Time.deltaTime);

                animator.SetFloat("clapPercent", clap_percent, 0.2f, Time.deltaTime);
            }
            clap_count--;
        }


        if (wave_count > 0)
        {
            if (wave_count < 15)
            {
                wave_percent = 0.4f;
                animator.SetFloat("wavePercent", wave_percent, 0.1f, Time.deltaTime);
            }
            else if (wave_count < 30)
            {
                wave_percent = 1;
                animator.SetFloat("wavePercent", wave_percent, 0.1f, Time.deltaTime);
            }
            else if (wave_count < 45)
            {
                wave_percent = 0.4f;
                up_percent = 0.5f;
                clap_percent = 0;
                animator.SetFloat("upPercent", up_percent, 0.01f, Time.deltaTime);
                animator.SetFloat("clapPercent", clap_percent, 0.01f, Time.deltaTime);

                animator.SetFloat("wavePercent", wave_percent, 0.1f, Time.deltaTime);
            }
            else
            {
                wave_percent = 1;
                up_percent = 0.5f;
                clap_percent = 0;
                animator.SetFloat("upPercent", up_percent, 0.01f, Time.deltaTime);
                animator.SetFloat("clapPercent", clap_percent, 0.01f, Time.deltaTime);

                animator.SetFloat("wavePercent", wave_percent, 0.2f, Time.deltaTime);
            }
            wave_count--;
        }

    }

    private void OnDestroy()
    {
        _netMqListener.Stop();
    }
}
