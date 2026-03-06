async function testCivicModel() {
  console.log('Testing Custom Civic ML Model (Nevesh06/Blaze)...\n');
  const SPACE_URL = 'https://nevesh06-blaze.hf.space';

  try {
    // 1. Fetch a real test image (Lorem Picsum always returns a proper JPEG)
    const testImageUrl = 'https://picsum.photos/seed/pothole/400/300.jpg';
    console.log('Fetching test image...');
    const imgRes = await fetch(testImageUrl);
    const imgBuffer = Buffer.from(await imgRes.arrayBuffer());
    console.log('\u2705 Test image fetched (', imgBuffer.length, 'bytes)');

    // 2. Upload image to the Space
    console.log('Uploading to Space...');
    const form = new FormData();
    form.append('files', new Blob([imgBuffer], { type: 'image/jpeg' }), 'pothole.jpg');
    const [uploadedPath] = await fetch(SPACE_URL + '/gradio_api/upload', { method: 'POST', body: form }).then(r => r.json());
    const fileUrl = `${SPACE_URL}/gradio_api/file=${uploadedPath}`;
    console.log('\u2705 Uploaded. File URL:', fileUrl);

    // 3. Call /predict_issue via REST queue (this is what works with public URLs)
    console.log('\nCalling Civic ML Model...');
    const sessionHash = Math.random().toString(36).substring(2, 10);
    const queueBody = {
      fn_index: 2,
      data: [{ path: fileUrl, url: fileUrl, orig_name: 'pothole.jpg', meta: { _type: 'gradio.FileData' } }],
      session_hash: sessionHash,
      event_data: null
    };
    await fetch(SPACE_URL + '/gradio_api/queue/join', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(queueBody)
    });
    const sseText = await fetch(`${SPACE_URL}/gradio_api/queue/data?session_hash=${sessionHash}`).then(r => r.text());
    // Parse SSE to find process_completed
    let result = null;
    for (const line of sseText.split('\n')) {
      if (!line.startsWith('data:')) continue;
      try {
        const msg = JSON.parse(line.slice(5).trim());
        if (msg.msg === 'process_completed' && msg.success && msg.output?.data?.[0]) {
          result = { data: msg.output.data };
          break;
        }
      } catch (_) {}
    }

    // 5. Output the results
    if (result && result.data) {
      console.log('✅ ML Model is WORKING! Detected Issue:\n');
      
      // Gradio wraps the return JSON in an array, so we grab data[0]
      const prediction = result.data[0]; 
      
      console.log(`   🚨 Issue: ${prediction.issue}`);
      console.log(`   🏢 Department: ${prediction.department}`);
      console.log(`   📊 Confidence: ${(prediction.confidence * 100).toFixed(1)}%`);
      
    } else {
      console.log('⚠️ API responded but returned no data');
    }

  } catch (err) {
    console.log('❌ ML API test FAILED');
    console.log('   Error:', err.message);
  }
}

testCivicModel();