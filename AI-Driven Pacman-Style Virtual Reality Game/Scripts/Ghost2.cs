using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Ghost2 : MonoBehaviour
{

    private UnityEngine.AI.NavMeshAgent ghost;

    public Transform PlayerTarget;
    // Start is called before the first frame update
    void Start()
    {
        ghost = GetComponent<UnityEngine.AI.NavMeshAgent>();
    }

    // Update is called once per frame
    void Update()
    {
        ghost.SetDestination(PlayerTarget.position);
    }
}