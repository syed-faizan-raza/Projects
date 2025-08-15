using System.Collections;
using System.Collections.Generic;
using UnityEngine;


public class Coco : MonoBehaviour
{
    private void OnTriggerEnter(Collider other)
    {
        if (other.CompareTag("Player"))
        {
            // Add points to the player
            PlayerScore.AddPoints(1);

            // Deactivate the coco object
            gameObject.SetActive(false);
        }
    }
}
