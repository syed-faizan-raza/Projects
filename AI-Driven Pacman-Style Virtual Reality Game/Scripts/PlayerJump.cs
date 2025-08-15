using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.InputSystem;

public class PlayerJump : MonoBehaviour
{
    [SerializeField] private InputActionProperty jumpButton;
    [SerializeField] private float jumpHeight = 3f;
    [SerializeField] private CharacterController cc;
    [SerializeField] private LayerMask groundLayers;

    private float gravity;
    private Vector3 movement;

    private void Start()
    {
        gravity = Physics.gravity.y; // Set gravity to the actual value of gravity
    }

    private void Update()
    {
        bool isGrounded = OnGround();

        if (jumpButton.action.WasPressedThisFrame() && isGrounded)
        {
            Jump();
        }

        movement.y += gravity * Time.deltaTime;
        cc.Move(movement * Time.deltaTime);
    }

    private void Jump()
    {
        movement.y = Mathf.Sqrt(jumpHeight * -3.0f * gravity);
    }

    private bool OnGround()
    {
        return Physics.CheckSphere(transform.position, 0.2f, groundLayers);
    }
}
