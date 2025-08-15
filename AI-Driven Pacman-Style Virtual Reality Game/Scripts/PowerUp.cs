using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class PowerUp : MonoBehaviour
{
    public float immunityDuration = 10f; // Duration of immunity in seconds

    private void OnTriggerEnter(Collider other)
    {
        if (other.CompareTag("Player"))
        {
            other.GetComponent<PlayerCollision>().ActivateImmunity(immunityDuration);
            gameObject.SetActive(false); // Deactivate power-up
        }
    }
}
