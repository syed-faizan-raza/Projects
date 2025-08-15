using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.AI;

public class GhostReturn : MonoBehaviour
{
    public Vector3 resetPosition; // Set this position in the Inspector
    private NavMeshAgent ghostAgent;

    void Start()
    {
        ghostAgent = GetComponent<NavMeshAgent>();
    }

    public void ResetPosition()
    {
        if (ghostAgent != null)
        {
            ghostAgent.Warp(resetPosition); // Warp the ghost to the reset position
        }
        else
        {
            transform.position = resetPosition; // Fallback if no NavMeshAgent
        }
    }
}
