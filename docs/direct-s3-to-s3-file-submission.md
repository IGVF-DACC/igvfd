# Direct S3-to-S3 File Submission

For labs submitting large volumes of files, the portal can transfer files bucket-to-bucket within AWS, directly from your S3 bucket into ours — no intermediate upload step.

This is opt-in and requires a one-time setup on both sides.

## Who this is for

Labs that keep their data in their own S3 bucket, where downloading and re-uploading through an extra step is slow, impractical, or expensive.

If you don't have your own S3 bucket, or you're only submitting a handful of small files, the regular upload flow is simpler.

## How it works

When you request upload credentials through the portal, you get short-lived AWS credentials scoped to write to one specific path in our bucket. Once your bucket is registered with us, those same credentials can *also* read from your bucket — so the copy runs directly S3-to-S3.

Registered submission buckets are scoped to a specific lab, not shared globally. The credentials issued for a given file can only read from buckets registered to *that file's submitting lab*.

Setup has two parts: we associate your bucket(s) with your lab on our side, and you grant our upload users read access on yours.

## Setup (one-time)

### Step 1 — Tell us your buckets

Contact your wrangler with the name(s) of the S3 bucket(s) you'll submit from.

We'll register them against your lab on our end and confirm when it's done.

### Step 2 — Grant us read access

In the S3 console, go to **your bucket → Permissions → Bucket Policy** and add the statement below. If your bucket already has a policy, add this as an additional statement — don't replace what's already there.

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowIGVFPortalUploadUsersRead",
      "Effect": "Allow",
      "Principal": {
        "AWS": [
          "arn:aws:iam::035226225042:user/upload-igvf-files",
          "arn:aws:iam::035226225042:user/upload-igvf-restricted-files",
          "arn:aws:iam::920073238245:user/upload-igvf-files",
          "arn:aws:iam::920073238245:user/upload-igvf-restricted-files"
        ]
      },
      "Action": [
        "s3:GetObject"
      ],
      "Resource": [
        "arn:aws:s3:::your-bucket-name/*"
      ]
    }
  ]
}
```

Which principals you need:

| Principal | Environment | Keep it if |
| --- | --- | --- |
| `035226225042:user/upload-igvf-files` | Production | Always — real submissions go through `api.data.igvf.org` |
| `035226225042:user/upload-igvf-restricted-files` | Production | You submit controlled-access files |
| `920073238245:user/upload-igvf-files` | Staging | You're testing against `api.staging.igvf.org` first |
| `920073238245:user/upload-igvf-restricted-files` | Staging | You're testing against staging *and* submit controlled-access files |

Leaving principals you don't currently need in place is harmless — it just saves you editing this policy again if what you submit changes later.

## Submitting files

Once setup is complete on both sides, request upload credentials through the portal the same way you do today. The response carries everything you need under `upload_credentials`:

- `access_key`, `secret_key`, `session_token` — the temporary credentials
- `upload_url` — the exact `s3://` destination for this one file
- `expiration` — when the credentials stop working

To test access with the AWS CLI, export the credentials and run the copy in the same shell session:

```bash
export AWS_ACCESS_KEY_ID=<ACCESS_KEY>
export AWS_SECRET_ACCESS_KEY=<SECRET_KEY>
export AWS_SESSION_TOKEN=<SESSION_TOKEN>

aws s3 cp s3://your-bucket-name/file.fastq.gz <UPLOAD_URL>
```

Three things to watch for:

- **All three exports are required.** These are temporary federated credentials, not a regular access key/secret pair, so `AWS_SESSION_TOKEN` must be set alongside the other two or the request will fail.
- **Don't pass `--profile`, and make sure `AWS_PROFILE` isn't set.** Either one takes precedence over these exports, and the copy will silently run as your own credentials instead.
- **One file per set of credentials.** Each set is valid only for the destination in `upload_url`, so copy one file at a time — `aws s3 sync` isn't supported.

Credentials are valid for **18 hours**.

## Troubleshooting

**`AccessDenied` reading from your bucket** — usually one of:

- A `Principal` ARN in your bucket policy doesn't exactly match one listed in Step 2 (check for typos)
- The bucket name in `Resource` doesn't match the bucket you're copying from
- You're submitting against production but only added the staging principals, or the reverse
- Your bucket registration hasn't been confirmed yet
- The file's submitting lab isn't the lab your bucket is registered under — buckets are registered per lab, so one lab's bucket won't grant access for another lab's files

**`AccessDenied` writing to our bucket** — your credentials have expired, or the destination doesn't match `upload_url`. Request a fresh set and copy that value verbatim.

## Questions

Contact your wrangler.
