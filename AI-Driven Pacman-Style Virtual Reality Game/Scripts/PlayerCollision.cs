using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;
using UnityEngine.XR.Interaction.Toolkit;

public class PlayerCollision : MonoBehaviour
{
    public bool isImmune = false;
    private float immunityTime = 0f;
    public float invincibleSpeed = 8f; // Speed during invincibility

    private ActionBasedContinuousMoveProvider moveProvider;
    private float originalSpeed;

    void Start()
    {
        moveProvider = GetComponent<ActionBasedContinuousMoveProvider>();
        if (moveProvider != null)
        {
            originalSpeed = moveProvider.moveSpeed;
        }
    }

    public void ActivateImmunity(float duration)
    {
        isImmune = true;
        immunityTime = duration;
        if (moveProvider != null)
        {
            moveProvider.moveSpeed = invincibleSpeed;
        }
    }

    private void Update()
    {
        if (isImmune)
        {
            immunityTime -= Time.deltaTime;
            if (immunityTime <= 0)
            {
                isImmune = false;
                if (moveProvider != null)
                {
                    moveProvider.moveSpeed = originalSpeed;
                }
            }
        }
    }

    private void OnTriggerEnter(Collider other)
    {
        if (other.CompareTag("Ghost"))
        {
            if (isImmune)
            {
                other.GetComponent<GhostReturn>().ResetPosition();
            }
            else
            {
                SceneManager.LoadScene("GameEnd");
            }
        }
    }
}
