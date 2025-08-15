using System.Collections;
using System.Collections.Generic;
using UnityEngine;


public class PlayerScore : MonoBehaviour
{
    public static int score = 0;

    public static void AddPoints(int points)
    {
        score += points;
        // Update UI or perform other actions
        Debug.Log("Score: " + score);
    }
}
