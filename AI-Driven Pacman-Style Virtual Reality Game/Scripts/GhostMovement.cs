using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.AI;

public class GhostMovement : MonoBehaviour
{
    private NavMeshAgent ghost;
    public Transform PlayerTarget;

    public float minRandomMovementDuration = 3.0f;
    public float maxRandomMovementDuration = 7.0f;
    public float minFollowPlayerChance = 0.5f;
    public float maxFollowPlayerChance = 0.9f;

    private float timer;
    private bool isFollowingPlayer = true;

    void Start()
    {
        ghost = GetComponent<NavMeshAgent>();
        SetRandomTimerAndBehavior();
    }

    void Update()
    {
        timer -= Time.deltaTime;

        if (timer <= 0.0f)
        {
            SetRandomTimerAndBehavior();

            if (isFollowingPlayer)
            {
                ghost.SetDestination(PlayerTarget.position);
            }
            else
            {
                Vector3 randomDestination = GetRandomDestination();
                ghost.SetDestination(randomDestination);
            }
        }
    }

    void SetRandomTimerAndBehavior()
    {
        timer = Random.Range(minRandomMovementDuration, maxRandomMovementDuration);
        isFollowingPlayer = Random.value < Random.Range(minFollowPlayerChance, maxFollowPlayerChance);
    }

    Vector3 GetRandomDestination()
    {
        Vector3 randomPosition = transform.position + new Vector3(Random.Range(-10f, 10f), 0f, Random.Range(-10f, 10f));
        NavMeshHit hit;

        if (NavMesh.SamplePosition(randomPosition, out hit, 10f, NavMesh.AllAreas))
        {
            return hit.position;
        }

        return GetRandomDestination();
    }
}
