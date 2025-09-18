import { NextResponse } from 'next/server';
import { getServerSession } from 'next-auth/next';
import {
  AccessToken,
  AgentDispatchClient,
  type AccessTokenOptions,
  type VideoGrant,
} from 'livekit-server-sdk';
import { authOptions } from '../auth/[...nextauth]/route';

// NOTE: you are expected to define the following environment variables in `.env.local`:
const API_KEY = process.env.LIVEKIT_API_KEY;
const API_SECRET = process.env.LIVEKIT_API_SECRET;
const LIVEKIT_URL = process.env.LIVEKIT_URL;

// don't cache the results
export const revalidate = 0;

export type ConnectionDetails = {
  serverUrl: string;
  roomName: string;
  participantName: string;
  participantToken: string;
};

export async function POST(req: Request) {
  try {
    const session = await getServerSession(authOptions);

    if (!session || !session.user || !session.user.name) {
      return new NextResponse('Unauthorized', { status: 401 });
    }

    if (LIVEKIT_URL === undefined) {
      throw new Error('LIVEKIT_URL is not defined');
    }
    if (API_KEY === undefined) {
      throw new Error('LIVEKIT_API_KEY is not defined');
    }
    if (API_SECRET === undefined) {
      throw new Error('LIVEKIT_API_SECRET is not defined');
    }

    const agentClient = new AgentDispatchClient(LIVEKIT_URL, API_KEY, API_SECRET);
    const roomName = `voice_assistant_room_${session.user.name.replace(' ', '_')}`;
    const agentName = `aria_agent_${session.user.name.replace(' ', '_')}`;
    await agentClient.createDispatch(roomName, agentName, { metadata: JSON.stringify({ purpose: 'voice-assistant' }) });

    const participantName = session.user.name;
    const participantIdentity = session.user.email!;

    const participantToken = await createParticipantToken(
      { identity: participantIdentity, name: participantName },
      roomName
    );

    const data: ConnectionDetails = {
      serverUrl: LIVEKIT_URL,
      roomName,
      participantToken: participantToken,
      participantName,
    };
    const headers = new Headers({
      'Cache-Control': 'no-store',
    });
    return NextResponse.json(data, { headers });
  } catch (error) {
    if (error instanceof Error) {
      console.error(error);
      return new NextResponse(error.message, { status: 500 });
    }
  }
}

function createParticipantToken(
  userInfo: AccessTokenOptions,
  roomName: string
): Promise<string> {
  const at = new AccessToken(API_KEY, API_SECRET, {
    ...userInfo,
    ttl: '15m',
  });
  const grant: VideoGrant = {
    room: roomName,
    roomJoin: true,
    canPublish: true,
    canPublishData: true,
    canSubscribe: true,
  };
  at.addGrant(grant);

  // We no longer need the agent configuration on the participant token,
  // as the job dispatch handles it. This can be removed.

  return at.toJwt();
}
