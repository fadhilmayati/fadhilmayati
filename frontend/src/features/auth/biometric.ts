import { getSupabaseClient } from './supabaseClient';

export interface BiometricCredential {
  deviceId: string;
  publicKey: string;
}

export async function enrolBiometric(deviceName: string): Promise<BiometricCredential> {
  if (!window.PublicKeyCredential) {
    throw new Error('WebAuthn is not supported on this device');
  }

  const challenge = crypto.getRandomValues(new Uint8Array(32));
  const credential = (await navigator.credentials.create({
    publicKey: {
      challenge,
      rp: { name: 'Dompet' },
      user: {
        id: crypto.getRandomValues(new Uint8Array(32)),
        name: deviceName,
        displayName: deviceName,
      },
      pubKeyCredParams: [{ type: 'public-key', alg: -7 }],
      authenticatorSelection: { userVerification: 'preferred' },
      timeout: 60000,
    },
  })) as PublicKeyCredential;

  const response = credential.response as AuthenticatorAttestationResponse;
  const publicKey = bufferToBase64(response.attestationObject);
  return {
    deviceId: credential.id,
    publicKey,
  };
}

export async function registerBiometricWithBackend(credential: BiometricCredential) {
  const supabase = getSupabaseClient();
  const session = await supabase.auth.getSession();
  if (!session.data.session?.access_token) {
    throw new Error('User must be authenticated');
  }

  const response = await fetch('/api/auth/biometric/enrol', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${session.data.session.access_token}`,
    },
    body: JSON.stringify({
      device_id: credential.deviceId,
      public_key: credential.publicKey,
    }),
  });

  if (!response.ok) {
    throw new Error('Failed to register biometric device');
  }
}

function bufferToBase64(buffer: ArrayBuffer) {
  const bytes = new Uint8Array(buffer);
  let binary = '';
  bytes.forEach((b) => {
    binary += String.fromCharCode(b);
  });
  return window.btoa(binary);
}
